package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.process.computer.MemoryComputeKey;
import org.apache.tinkerpop.gremlin.process.traversal.Order;
import org.apache.tinkerpop.gremlin.process.traversal.Traversal;
import org.apache.tinkerpop.gremlin.process.traversal.Traverser;
import org.apache.tinkerpop.gremlin.process.traversal.lambda.IdentityTraversal;
import org.apache.tinkerpop.gremlin.process.traversal.step.ByModulating;
import org.apache.tinkerpop.gremlin.process.traversal.step.ComparatorHolder;
import org.apache.tinkerpop.gremlin.process.traversal.step.TraversalParent;
import org.apache.tinkerpop.gremlin.process.traversal.step.util.CollectingBarrierStep;
import org.apache.tinkerpop.gremlin.process.traversal.traverser.ProjectedTraverser;
import org.apache.tinkerpop.gremlin.process.traversal.traverser.TraverserRequirement;
import org.apache.tinkerpop.gremlin.process.traversal.traverser.util.TraverserSet;
import org.apache.tinkerpop.gremlin.process.traversal.util.TraversalUtil;
import org.apache.tinkerpop.gremlin.structure.util.StringFactory;
import org.apache.tinkerpop.gremlin.util.function.MultiComparator;
import org.javatuples.Pair;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.function.BinaryOperator;
import java.util.stream.Collectors;

// from: https://raw.githubusercontent.com/apache/tinkerpop/3.4.6/gremlin-core/src/main/java/org/apache/tinkerpop/gremlin/process/traversal/step/map/OrderGlobalStep.java
public final class OrderGlobalStepAcceptNull<S, C extends Comparable> extends CollectingBarrierStep<S> implements ComparatorHolder<S, C>, TraversalParent, ByModulating {

    private List<Pair<Traversal.Admin<S, C>, Comparator<C>>> comparators = new ArrayList<>();
    private MultiComparatorAcceptNull<C> multiComparator = null;
    private long limit = Long.MAX_VALUE;

    public OrderGlobalStepAcceptNull(final Traversal.Admin traversal, long limit) {
        super(traversal);
        this.limit = limit;
    }

    @Override
    public void barrierConsumer(final TraverserSet<S> traverserSet) {
        if (null == this.multiComparator) this.multiComparator = this.createMultiComparator();
        //
        if (this.multiComparator.isShuffle())
            traverserSet.shuffle();
        else
            traverserSet.sort((Comparator) this.multiComparator);
    }

    @Override
    public void processAllStarts() {
        while (this.starts.hasNext()) {
            this.traverserSet.add(this.createProjectedTraverser(this.starts.next()));
        }
    }

    public void setLimit(final long limit) {
        this.limit = limit;
    }

    public long getLimit() {
        return this.limit;
    }

    @Override
    public void addComparator(final Traversal.Admin<S, C> traversal, final Comparator<C> comparator) {
        this.comparators.add(new Pair<>(this.integrateChild(traversal), comparator));
    }

    @Override
    public void modulateBy(final Traversal.Admin<?, ?> traversal) {
        this.modulateBy(traversal, Order.asc);
    }

    @Override
    public void modulateBy(final Traversal.Admin<?, ?> traversal, final Comparator comparator) {
        this.addComparator((Traversal.Admin<S, C>) traversal, comparator);
    }

    @Override
    public List<Pair<Traversal.Admin<S, C>, Comparator<C>>> getComparators() {
        return this.comparators.isEmpty() ? Collections.singletonList(new Pair<>(new IdentityTraversal(), (Comparator) Order.asc)) : Collections.unmodifiableList(this.comparators);
    }

    @Override
    public String toString() {
        return StringFactory.stepString(this, this.comparators);
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        for (int i = 0; i < this.comparators.size(); i++) {
            result ^= this.comparators.get(i).hashCode() * (i + 1);
        }
        return result;
    }

    @Override
    public Set<TraverserRequirement> getRequirements() {
        return this.getSelfAndChildRequirements(TraverserRequirement.BULK, TraverserRequirement.OBJECT);
    }

    @Override
    public List<Traversal.Admin<S, C>> getLocalChildren() {
        return (List) this.comparators.stream().map(Pair::getValue0).collect(Collectors.toList());
    }

    @Override
    public OrderGlobalStepAcceptNull<S, C> clone() {
        final OrderGlobalStepAcceptNull<S, C> clone = (OrderGlobalStepAcceptNull<S, C>) super.clone();
        clone.comparators = new ArrayList<>();
        for (final Pair<Traversal.Admin<S, C>, Comparator<C>> comparator : this.comparators) {
            clone.comparators.add(new Pair<>(comparator.getValue0().clone(), comparator.getValue1()));
        }
        return clone;
    }

    @Override
    public void setTraversal(final Traversal.Admin<?, ?> parentTraversal) {
        super.setTraversal(parentTraversal);
        this.comparators.stream().map(Pair::getValue0).forEach(TraversalParent.super::integrateChild);
    }

    @Override
    public MemoryComputeKey<TraverserSet<S>> getMemoryComputeKey() {
        if (null == this.multiComparator) this.multiComparator = this.createMultiComparator();
        return MemoryComputeKey.of(this.getId(), new OrderGlobalStepAcceptNull.OrderBiOperator<>(this.limit, this.multiComparator), false, true);
    }

    private final ProjectedTraverser<S, C> createProjectedTraverser(final Traverser.Admin<S> traverser) {
        final List<C> projections = new ArrayList<>(this.comparators.size());
        for (final Pair<Traversal.Admin<S, C>, Comparator<C>> pair : this.comparators) {
            try {
                projections.add(TraversalUtil.apply(traverser, pair.getValue0()));
            } catch(IllegalStateException e) {
                projections.add(null);
            }
        }
        return new ProjectedTraverser<>(traverser, projections);
    }

    private final MultiComparatorAcceptNull<C> createMultiComparator() {
        final List<Comparator<C>> list = new ArrayList<>(this.comparators.size());
        for (final Pair<Traversal.Admin<S, C>, Comparator<C>> pair : this.comparators) {
            list.add(pair.getValue1());
        }
        return new MultiComparatorAcceptNull<>(list);
    }

    ////////////////

    public static final class OrderBiOperator<S> implements BinaryOperator<TraverserSet<S>>, Serializable {

        private long limit;
        private MultiComparatorAcceptNull comparator;

        private OrderBiOperator() {
            // for serializers that need a no-arg constructor
        }

        public OrderBiOperator(final long limit, final MultiComparatorAcceptNull multiComparator) {
            this.limit = limit;
            this.comparator = multiComparator;
        }

        @Override
        public TraverserSet<S> apply(final TraverserSet<S> setA, final TraverserSet<S> setB) {
            setA.addAll(setB);
            if (this.limit != -1 && setA.bulkSize() > this.limit) {
                if (this.comparator.isShuffle())
                    setA.shuffle();
                else
                    setA.sort(this.comparator);
                long counter = 0L;
                final Iterator<Traverser.Admin<S>> traversers = setA.iterator();
                while (traversers.hasNext()) {
                    final Traverser.Admin<S> traverser = traversers.next();
                    if (counter > this.limit)
                        traversers.remove();
                    counter = counter + traverser.bulk();
                }
            }
            return setA;
        }
    }
}
