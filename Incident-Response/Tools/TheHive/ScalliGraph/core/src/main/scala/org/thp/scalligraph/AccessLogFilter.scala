package org.thp.scalligraph

import akka.stream.Materializer
import javax.inject.Inject
import play.api.Logger
import play.api.http.{DefaultHttpFilters, EnabledFilters}
import play.api.mvc._

import scala.concurrent.ExecutionContext

class AccessLogFilter @Inject() (implicit val mat: Materializer, ec: ExecutionContext, errorHandler: ErrorHandler) extends EssentialFilter {

  val logger: Logger = Logger(getClass)

  override def apply(next: EssentialAction): EssentialAction =
    (requestHeader: RequestHeader) => {
      val startTime = System.currentTimeMillis
      DiagnosticContext
        .withRequest(requestHeader)(next(requestHeader))
        .recoverWith { case error => errorHandler.onServerError(requestHeader, error) }
        .map { result =>
          DiagnosticContext.withRequest(requestHeader) {
            val endTime     = System.currentTimeMillis
            val requestTime = endTime - startTime

            logger.info(
              s"${requestHeader.remoteAddress} ${requestHeader.method} ${requestHeader.uri} took ${requestTime}ms and returned ${result.header.status} ${result
                .body
                .contentLength
                .fold("")(_ + " bytes")}"
            )

            result.withHeaders("Request-Time" -> requestTime.toString)
          }
        }
    }
}

class Filters @Inject() (enabledFilters: EnabledFilters, accessLogFilter: AccessLogFilter)
    extends DefaultHttpFilters(enabledFilters.filters :+ accessLogFilter: _*)
