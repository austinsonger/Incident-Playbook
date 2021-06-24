package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.process.traversal.Traversal;
import org.apache.tinkerpop.gremlin.process.traversal.TraversalStrategy;
import org.apache.tinkerpop.gremlin.process.traversal.step.map.OrderGlobalStep;
import org.apache.tinkerpop.gremlin.process.traversal.strategy.AbstractTraversalStrategy;
import org.apache.tinkerpop.gremlin.process.traversal.util.TraversalHelper;
import org.javatuples.Pair;

import java.util.Comparator;

public final class OrderAcceptNullStrategy extends AbstractTraversalStrategy<TraversalStrategy.OptimizationStrategy> implements TraversalStrategy.OptimizationStrategy {

    private static final OrderAcceptNullStrategy INSTANCE = new OrderAcceptNullStrategy();

    private OrderAcceptNullStrategy() {
    }

    @Override
    public void apply(final Traversal.Admin<?, ?> traversal) {
        TraversalHelper.getStepsOfClass(OrderGlobalStep.class, traversal).forEach((originalStep) -> {
            OrderGlobalStepAcceptNull step = new OrderGlobalStepAcceptNull(originalStep.getTraversal(), originalStep.getLimit());
            originalStep.getComparators().forEach((pairObj) -> {
                Pair<Traversal.Admin, Comparator> comparatorPair = (Pair<Traversal.Admin, Comparator>)pairObj;
                step.addComparator(comparatorPair.getValue0(), comparatorPair.getValue1());
            });
            TraversalHelper.replaceStep(originalStep, step, traversal);
        });
    }

    public static OrderAcceptNullStrategy instance() {
        return INSTANCE;
    }
}
