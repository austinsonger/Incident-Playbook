package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.structure.Element;
import org.apache.tinkerpop.gremlin.structure.Property;

import java.io.Serializable;
import java.util.Comparator;

public final class ElementValueComparatorAcceptNull<V> implements Comparator<Element>, Serializable {

    private final String propertyKey;
    private final Comparator<V> valueComparator;

    public ElementValueComparatorAcceptNull(final String propertyKey, final Comparator<V> valueComparator) {
        this.propertyKey = propertyKey;
        this.valueComparator = valueComparator;
    }

    public String getPropertyKey() {
        return this.propertyKey;
    }

    public Comparator<V> getValueComparator() {
        return this.valueComparator;
    }

    @Override
    public int compare(final Element elementA, final Element elementB) {
//        return this.valueComparator.compare(elementA.value(this.propertyKey), elementB.value(this.propertyKey));
        Property<V> propA = elementA.property(this.propertyKey);
        Property<V> propB = elementB.property(this.propertyKey);
        if (propA.isPresent() && propB.isPresent()) return this.valueComparator.compare(propA.value(), propB.value());
        else if (propA.isPresent()) return -1;
        else if (propB.isPresent()) return 1;
        else return 0;

    }

    @Override
    public String toString() {
        return this.valueComparator.toString() + "AcceptNull(" + this.propertyKey + ')';
    }
}
