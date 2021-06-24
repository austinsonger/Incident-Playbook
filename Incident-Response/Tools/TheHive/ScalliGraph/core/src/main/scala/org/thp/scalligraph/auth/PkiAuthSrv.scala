package org.thp.scalligraph.auth

import java.io.ByteArrayInputStream
import java.security.cert.X509Certificate
import java.util.{List => JList}

import javax.inject.{Inject, Singleton}
import javax.naming.ldap.LdapName
import org.bouncycastle.asn1._
import play.api.Configuration
import play.api.mvc.Request

import scala.collection.JavaConverters._
import scala.concurrent.ExecutionContext
import scala.util.Try

class PkiAuthSrv(certificateField: String, requestOrganisation: RequestOrganisation, userSrv: UserSrv, val ec: ExecutionContext)
    extends AuthSrvWithActionFunction {
  override val name: String = "pki"

  @scala.annotation.tailrec
  final def asn1String(obj: ASN1Primitive): String = obj match {
    case ds: DERUTF8String    => DERUTF8String.getInstance(ds).getString
    case to: ASN1TaggedObject => asn1String(ASN1TaggedObject.getInstance(to).getObject)
    case os: ASN1OctetString  => new String(os.getOctets)
    case as: ASN1String       => as.getString
  }

  object CertificateSAN {

    def unapply(l: JList[_]): Option[(String, String)] = {
      val typeValue = for {
        t <- Option(l.get(0))
        v <- Option(l.get(1))
      } yield t -> v
      typeValue
        .collect { case (t: Integer, v) => t.toInt -> v }
        .collect {
          case (0, value: Array[Byte]) =>
            val asn1     = new ASN1InputStream(new ByteArrayInputStream(value)).readObject()
            val asn1Seq  = ASN1Sequence.getInstance(asn1)
            val id       = ASN1ObjectIdentifier.getInstance(asn1Seq.getObjectAt(0)).getId
            val valueStr = asn1String(asn1Seq.getObjectAt(1).toASN1Primitive)

            id match {
              case "1.3.6.1.4.1.311.20.2.3" => "upn" -> valueStr
              // Add other object id
              case other => other -> valueStr
            }
          case (1, value: String) => "rfc822Name"                -> value
          case (2, value: String) => "dNSName"                   -> value
          case (3, value: String) => "x400Address"               -> value
          case (4, value: String) => "directoryName"             -> value
          case (5, value: String) => "ediPartyName"              -> value
          case (6, value: String) => "uniformResourceIdentifier" -> value
          case (7, value: String) => "iPAddress"                 -> value
          case (8, value: String) => "registeredID"              -> value
        }
    }
  }

  def extractFieldFromSubject(cert: X509Certificate): Option[String] = {
    val dn       = cert.getSubjectX500Principal.getName
    val ldapName = new LdapName(dn)
    ldapName
      .getRdns
      .asScala
      .collectFirst {
        case rdn if rdn.getType == certificateField => rdn.getValue.toString
      }
  }

  def extractFieldFromSAN(cert: X509Certificate): Option[String] =
    for {
      san <- Option(cert.getSubjectAlternativeNames)
      fieldValue <- san.asScala.collectFirst {
        case CertificateSAN(`certificateField`, value) => value
      }
    } yield fieldValue

  override def getAuthContext[A](request: Request[A]): Option[AuthContext] =
    request
      .clientCertificateChain
      .flatMap(_.headOption)
      .flatMap { cert =>
        extractFieldFromSubject(cert)
          .orElse(extractFieldFromSAN(cert))
          .flatMap(userId => userSrv.getAuthContext(request, userId, requestOrganisation(request)).toOption)
      }
}

@Singleton
class PkiAuthProvider @Inject() (requestOrganisation: RequestOrganisation, userSrv: UserSrv, ec: ExecutionContext) extends AuthSrvProvider {
  override val name: String = "pki"
  override def apply(config: Configuration): Try[AuthSrv] =
    for {
      certificateField <- config.getOrFail[String]("certificateField")
    } yield new PkiAuthSrv(certificateField, requestOrganisation, userSrv, ec)
}
