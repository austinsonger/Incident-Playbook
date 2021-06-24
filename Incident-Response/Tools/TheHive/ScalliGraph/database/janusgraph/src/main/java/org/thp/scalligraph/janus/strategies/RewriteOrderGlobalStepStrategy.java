//package org.thp.scalligraph.janus.strategies;
//
//import org.apache.tinkerpop.gremlin.process.traversal.Order;
//import org.apache.tinkerpop.gremlin.process.traversal.Traversal;
//import org.apache.tinkerpop.gremlin.process.traversal.TraversalStrategy;
//import org.apache.tinkerpop.gremlin.process.traversal.Traverser;
//import org.apache.tinkerpop.gremlin.process.traversal.lambda.AbstractLambdaTraversal;
//import org.apache.tinkerpop.gremlin.process.traversal.lambda.ElementValueTraversal;
//import org.apache.tinkerpop.gremlin.process.traversal.step.map.OrderGlobalStep;
//import org.apache.tinkerpop.gremlin.process.traversal.util.TraversalHelper;
//import org.apache.tinkerpop.gremlin.process.traversal.util.TraversalUtil;
//import org.apache.tinkerpop.gremlin.structure.Element;
//import org.javatuples.Pair;
//
//import java.util.Comparator;
//import java.util.List;
//import java.util.Set;
//
//public class RewriteOrderGlobalStepStrategy implements TraversalStrategy.OptimizationStrategy {
//    private static final RewriteOrderGlobalStepStrategy INSTANCE = new RewriteOrderGlobalStepStrategy();
//
//    private RewriteOrderGlobalStepStrategy() {
//    }
//
//    @Override
//    public void apply(final Traversal.Admin<?, ?> traversal) {
//        List<OrderGlobalStep> steps = TraversalHelper.getStepsOfAssignableClass(OrderGlobalStep.class, traversal);
//        for (OrderGlobalStep step : steps) {
//            if (step.getComparators().isEmpty()) {
//                continue;
//            }
//            List<Pair> comparators = step.getComparators();
//            OrderGlobalStep newStep = new OrderGlobalStep(traversal);
//            for (Pair pair : comparators) {
//                if (pair.getValue0() instanceof ElementValueTraversal && pair.getValue1() instanceof Order) {
//                    String propertyKey = ((ElementValueTraversal) pair.getValue0()).getPropertyKey();
//                    Order order = (Order) pair.getValue1();
//                    newStep.addComparator(new ElementValueTraversalDummy<>(propertyKey), new ComparatorWrapper(order));
//                } else if (pair.getValue1() instanceof Order) {
//                    Order order = (Order) pair.getValue1();
//                    newStep.addComparator((Traversal.Admin) pair.getValue0(), new ComparatorWrapper(order));
//                } else {
//                    newStep.addComparator((Traversal.Admin) pair.getValue0(), (Comparator) pair.getValue1());
//                }
//            }
//            Set<String> labels = step.getLabels();
//            labels.forEach(newStep::addLabel);
//            TraversalHelper.replaceStep(step, newStep, traversal);
//        }
//    }
//
//    public static RewriteOrderGlobalStepStrategy getInstance() {
//        return INSTANCE;
//    }
//
//    static class ElementValueTraversalDummy<T> extends AbstractLambdaTraversal<Element, T> {
//        private final String propertyKey;
//        private T value;
//
//        ElementValueTraversalDummy(final String propertyKey) {
//            this.propertyKey = propertyKey;
//        }
//
//        @Override
//        public T next() {
//            return this.value;
//        }
//
//        @Override
//        public boolean hasNext() {
//            return true;
//        }
//
//        @Override
//        public void addStart(final Traverser.Admin<Element> start) {
//            this.value = this.bypassTraversal == null ? (T) start.get().property(this.propertyKey).orElse(null)
//                    : TraversalUtil.apply(start, this.bypassTraversal);
//        }
//
//        @Override
//        public String toString() {
//            return "value(" + (this.bypassTraversal == null ? this.propertyKey : this.bypassTraversal) + ')';
//        }
//
//        @Override
//        @SuppressWarnings("EqualsHashCode")
//        public int hashCode() {
//            return super.hashCode() ^ this.propertyKey.hashCode();
//        }
//    }
//
//    public static class ComparatorWrapper implements Comparator<Object> {
//        private final Comparator<Object> comprator;
//
//        public ComparatorWrapper(Comparator<Object> comprator) {
//            this.comprator = comprator;
//        }
//
//        @Override
//        public int compare(final Object first, final Object second) {
//            if (first == null && second == null) {
//                return 0;
//            } else if (first == null) {
//                return 1;
//            } else if (second == null) {
//                return -1;
//            } else {
//                return comprator.compare(first, second);
//            }
//        }
//    }
//}
