import pytest
from pydantic import ValidationError

from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityGroupPlanV8,
    assignment_partitions,
)


def test_assignment_partitions_cover_dense_source_once() -> None:
    partitions = assignment_partitions(list(range(31)), 8)

    assert [requirements for requirements, _ in partitions] == [
        list(range(0, 8)),
        list(range(8, 16)),
        list(range(16, 24)),
        list(range(24, 31)),
    ]
    responsibilities = [index for _, bucket in partitions for index in bucket]
    assert sorted(responsibilities) == list(range(8))
    assert len(responsibilities) == len(set(responsibilities))


def test_dense_group_plan_requires_more_than_one_group() -> None:
    payload = {
        "role_interpretation": "A dense technical role with multiple work capability areas.",
        "groups": [
            {
                "group_id": 0,
                "capability_label": "One giant group",
                "summary": "A single catch-all group for all dense job facts.",
            }
        ],
        "uncertainties": [],
    }

    with pytest.raises(ValidationError, match="Dense jobs require at least two"):
        CapabilityGroupPlanV8.model_validate(
            payload,
            context={"capability_requirement_count": 31, "responsibility_count": 8},
        )


def test_assignment_partition_must_cover_exact_owned_indices_and_valid_groups() -> None:
    context = {
        "owned_requirement_indices": [4, 5],
        "owned_responsibility_indices": [1],
        "valid_group_ids": [0, 1],
    }
    valid = CapabilityAssignmentPartitionV8.model_validate(
        {
            "requirement_assignments": [
                {"index": 4, "group_ids": [0]},
                {"index": 5, "group_ids": [1]},
            ],
            "responsibility_assignments": [{"index": 1, "group_ids": [0, 1]}],
        },
        context=context,
    )
    assert [item.index for item in valid.requirement_assignments] == [4, 5]

    with pytest.raises(ValidationError, match="cover exactly its owned requirement"):
        CapabilityAssignmentPartitionV8.model_validate(
            {
                "requirement_assignments": [{"index": 4, "group_ids": [0]}],
                "responsibility_assignments": [{"index": 1, "group_ids": [0]}],
            },
            context=context,
        )

    with pytest.raises(ValidationError, match="unknown capability groups"):
        CapabilityAssignmentPartitionV8.model_validate(
            {
                "requirement_assignments": [
                    {"index": 4, "group_ids": [0]},
                    {"index": 5, "group_ids": [9]},
                ],
                "responsibility_assignments": [{"index": 1, "group_ids": [0]}],
            },
            context=context,
        )
