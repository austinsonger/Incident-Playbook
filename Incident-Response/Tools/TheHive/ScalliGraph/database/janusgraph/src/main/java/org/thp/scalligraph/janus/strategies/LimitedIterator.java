package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.structure.Element;

import java.util.Iterator;

public class LimitedIterator<E extends Element> implements Iterator<E> {

    final Iterator<E> iterator;
    int count = 0;
    final int highLimit;

    public LimitedIterator(final Integer lowLimit, final Integer highLimit, final Iterator<E> iterator) {
        this.iterator = iterator;
        this.highLimit = highLimit;
        while (iterator.hasNext() && count < lowLimit) {
            iterator.next();
            count++;
        }
    }

    @Override
    public boolean hasNext() {
        return count < this.highLimit && this.iterator.hasNext();
    }

    @Override
    public E next() {
        return this.iterator.next();
    }
}
