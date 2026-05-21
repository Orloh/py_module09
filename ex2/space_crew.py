#!/usr/bin/env python3
# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   space_crew.py                                      :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/05/18 17:33:53 by orhernan          #+#    #+#             #
#   Updated: 2026/05/18 17:33:53 by orhernan         ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError, InitErrorDetails
from datetime import datetime
from enum import Enum
from typing import Any


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':
        # Mission ID must start with 'M'
        errors: list[InitErrorDetails] = []

        if not self.mission_id.startswith('M'):
            errors.append(
                make_error(
                    "mission_id_error",
                    "ID must start with 'M'",
                    ("mission_id",),
                    self.mission_id
                )
            )

        # All crew memebers must bee active
        if not all(member.is_active for member in self.crew):
            errors.append(
                make_error(
                    "inactive_crew_error",
                    "Inactive creww memeber found",
                    ("crew",),
                    self.crew
                )
            )

        # Must have at least one Commander or Captaion
        has_leadership = any(
           member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
           for member in self.crew
        )
        if not has_leadership:
            errors.append(
                make_error(
                    "leadership_error",
                    "Missing Commander/Captain",
                    ("crew",),
                    self.crew
                )
            )

        # Long Missions (>365 days) need 50% experienced crew (+5 years)
        if self.duration_days > 365:
            exp_crew = [
                member for member in self.crew if member.years_experience >= 5
            ]
            if len(exp_crew) < (len(self.crew) / 2):
                errors.append(
                    make_error(
                        "inexperienced_crew_error",
                        "Inexperienced crew member found",
                        ("crew",),
                        self.crew
                    )
                )

        if errors:
            raise ValidationError.from_exception_data(
                self.__class__.__name__,
                errors
            )
        return self


def make_error(
        error_code: str,
        message: str,
        loc: tuple[int | str, ...],
        input: Any
) -> InitErrorDetails:
    return {
        "type": PydanticCustomError(error_code, message),
        "loc": loc,
        "input": input
    }


def print_validation_errors(exception: ValidationError) -> None:
    for error in exception.errors():
        type = error['type']
        message = error['msg']

        print(f"    • {type}: {message}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 80)

    # 1. Create a valid mission dataset
    valid_crew = [
        CrewMember(
            member_id="CMD01",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission Command",
            years_experience=11
        ),
        CrewMember(
            member_id="LT02",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=32,
            specialization="Navigation",
            years_experience=5
        ),
        CrewMember(
            member_id="OFF03",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=28,
            specialization="Engineering",
            years_experience=3
        )
    ]

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 10, 10, 12, 0),
            duration_days=900,
            crew=valid_crew,
            budget_millions=2500.0
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for m in valid_mission.crew:
            print(f"  - {m.name} ({m.rank.value}) - {m.specialization}")

    except ValidationError as e:
        print_validation_errors(e)

    print("\n" + "=" * 80)

    # 2. Attempt to create an invalid mission (Missing Captain or Commander)
    invalid_crew = [
        CrewMember(
            member_id="LT05",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=30,
            specialization="Navigation",
            years_experience=4
        ),
        CrewMember(
            member_id="OFF06",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=25,
            specialization="Engineering",
            years_experience=2
        )
    ]

    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Unled Exploration",
            destination="Moon",
            launch_date=datetime(2026, 6, 1),
            duration_days=500,
            crew=invalid_crew,
            budget_millions=150.0
        )
    except ValidationError as e:
        print_validation_errors(e)


if __name__ == "__main__":
    main()
