package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.process.traversal.Order;
import org.apache.tinkerpop.gremlin.process.traversal.traverser.ProjectedTraverser;

import java.io.Serializable;
import java.util.Comparator;
import java.util.List;

/**
 * @author Marko A. Rodriguez (http://markorodriguez.com)
 */
public final class MultiComparatorAcceptNull<C> implements Comparator<C>, Serializable {

    private List<Comparator> comparators;
    private boolean isShuffle;
    int startIndex = 0;

    private MultiComparatorAcceptNull() {
        // for serialization purposes
    }

    public MultiComparatorAcceptNull(final List<Comparator<C>> comparators) {
        this.comparators = (List) comparators;
        this.isShuffle = !this.comparators.isEmpty() && Order.shuffle == this.comparators.get(this.comparators.size() - 1);
        for (int i = 0; i < this.comparators.size(); i++) {
            if (this.comparators.get(i) == Order.shuffle)
                this.startIndex = i + 1;
        }
    }

    @Override
    public int compare(final C objectA, final C objectB) {
        if (this.comparators.isEmpty()) {
            return Order.asc.compare(objectA, objectB);
        } else {
            for (int i = this.startIndex; i < this.comparators.size(); i++) {
                Object a = this.getObject(objectA, i);
                Object b = this.getObject(objectB, i);
                if (a != null && b != null) {
                    final int comparison = this.comparators.get(i).compare(a, b);
                    if (comparison != 0)
                        return comparison;
                } else if (a != null)
                    return -1;
                else if (b != null)
                    return 1;
            }
            return 0;
        }
    }

    public boolean isShuffle() {
        return this.isShuffle;
    }

    private final Object getObject(final C object, final int index) {
        if (object instanceof ProjectedTraverser)
            return ((ProjectedTraverser) object).getProjections().get(index);
        else
            return object;
    }
}
