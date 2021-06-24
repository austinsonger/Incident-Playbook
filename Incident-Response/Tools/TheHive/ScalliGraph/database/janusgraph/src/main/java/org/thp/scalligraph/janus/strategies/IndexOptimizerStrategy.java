package org.thp.scalligraph.janus.strategies;

import org.apache.tinkerpop.gremlin.process.traversal.Step;
import org.apache.tinkerpop.gremlin.process.traversal.Traversal;
import org.apache.tinkerpop.gremlin.process.traversal.TraversalStrategy;
import org.apache.tinkerpop.gremlin.process.traversal.step.filter.HasStep;
import org.apache.tinkerpop.gremlin.process.traversal.step.filter.NotStep;
import org.apache.tinkerpop.gremlin.process.traversal.step.filter.TraversalFilterStep;
import org.apache.tinkerpop.gremlin.process.traversal.step.map.GraphStep;
import org.apache.tinkerpop.gremlin.process.traversal.step.map.OrderGlobalStep;
import org.apache.tinkerpop.gremlin.process.traversal.strategy.AbstractTraversalStrategy;
import org.apache.tinkerpop.gremlin.process.traversal.strategy.optimization.FilterRankingStrategy;
import org.apache.tinkerpop.gremlin.process.traversal.strategy.optimization.InlineFilterStrategy;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * {@code IndexOptimizerStrategy} reorders HasSteps, FilterSteps and OrderSteps that follow a GraphStep
 * HasSteps and OrderSteps are put just after GraphStep in order to use graph index
 */
public final class IndexOptimizerStrategy extends AbstractTraversalStrategy<TraversalStrategy.OptimizationStrategy> implements TraversalStrategy.OptimizationStrategy {

    private static final IndexOptimizerStrategy INSTANCE = new IndexOptimizerStrategy();
    private static final Set<Class<? extends OptimizationStrategy>> PRIORS = new HashSet<>(Arrays.asList(InlineFilterStrategy.class, FilterRankingStrategy.class));

    private IndexOptimizerStrategy() {
    }

    @Override
    public void apply(final Traversal.Admin<?, ?> traversal) {
        if (traversal.getStartStep() instanceof GraphStep) {
            apply(traversal, traversal.getSteps(), 1);
        }
    }

    private int apply(final Traversal.Admin<?, ?> traversal, List<Step> steps, int index) {
        if (index < steps.size()) {
            Step step = steps.get(index);
            if (step instanceof HasStep<?> || step instanceof OrderGlobalStep<?, ?>)
                return apply(traversal, steps, index + 1);
            else if (step instanceof TraversalFilterStep<?> || step instanceof NotStep<?>) {
                traversal.removeStep(index);
                int newPosition = apply(traversal, traversal.getSteps(), index);
                traversal.addStep(newPosition, step);
                return newPosition;
            } else
                return index;
        } else return index;
    }

    @Override
    public Set<Class<? extends OptimizationStrategy>> applyPrior() {
        return PRIORS;
    }

    public static IndexOptimizerStrategy instance() {
        return INSTANCE;
    }
}
