import pytest

from neetcode_references.ai import (
    CallBudget,
    CallBudgetExceeded,
)


def test_problem_budget_is_enforced():
    budget = CallBudget(
        run_limit=10,
        problem_limit=2,
    )

    budget.begin_problem()

    budget.consume()
    budget.consume()

    with pytest.raises(
        CallBudgetExceeded
    ):
        budget.consume()


def test_run_budget_is_enforced():
    budget = CallBudget(
        run_limit=2,
        problem_limit=10,
    )

    budget.begin_problem()
    budget.consume()
    budget.consume()

    budget.begin_problem()

    with pytest.raises(
        CallBudgetExceeded
    ):
        budget.consume()


def test_begin_problem_resets_problem_counter_only():
    budget = CallBudget(
        run_limit=10,
        problem_limit=3,
    )

    budget.begin_problem()
    budget.consume()
    budget.consume()

    assert budget.run_calls == 2
    assert budget.problem_calls == 2

    budget.begin_problem()

    assert budget.run_calls == 2
    assert budget.problem_calls == 0
