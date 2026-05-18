#!/usr/bin/env python3
# ************************************************************************** #
#                                                                            #
#                                                        :::      ::::::::   #
#   alien_contact.py                                   :+:      :+:    :+:   #
#                                                    +:+ +:+         +:+     #
#   By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+        #
#                                                +#+#+#+#+#+   +#+           #
#   Created: 2026/05/14 16:30:09 by orhernan          #+#    #+#             #
#   Updated: 2026/05/14 16:30:09 by orhernan         ###   ########.fr       #
#                                                                            #
# ************************************************************************** #

from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact_id(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must contain AC")
        return self

    @model_validator(mode='after')
    def validate_physical_contact(self) -> 'AlienContact':
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError('Physical contact reports must be verified')
        return self

    @model_validator(mode='after')
    def validate_telepathic_contact(self) -> 'AlienContact':
        if (
            self.contact_type == ContactType.TELEPATHIC and not
            self.witness_count >= 3
        ):
            raise ValueError(
                'Telepathic contact requires at least 3 witnesses'
            )
        return self

    @model_validator(mode='after')
    def validate_strong_signal(self) -> 'AlienContact':
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                'High signal strength requires a received message'
            )
        return self


def display_report(contact: AlienContact) -> None:
    minutes_label = "minute" if contact.duration_minutes == 1 else "minutes"

    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength:.1f}/10")
    print(f"Duration: {contact.duration_minutes} {minutes_label}")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {contact.message_received}")


def print_validation_errors(exception: ValidationError) -> None:
    for error in exception.errors():
        field = "->".join(str(loc) for loc in error['loc'])
        message = error['msg']

        print(f"    • {field}: {message}")


def main() -> None:
    print("Alien Contact Log Validation")

    try:
        valid_contact = AlienContact(
            contact_id="AC_2026_001",
            timestamp=datetime.now(),
            contact_type=ContactType.TELEPATHIC,
            location="42Madrid",
            signal_strength=6.5,
            duration_minutes=92,
            witness_count=4,
            message_received="E.T Phone Earth"
        )
        print("Valid contact report:")
        display_report(valid_contact)

    except ValidationError as e:
        print("Unexpected Error:")
        print_validation_errors(e)

    print("\nExpected validation error:")
    try:
        invalid_contact = AlienContact(
            contact_id="AC_2026_002",
            timestamp=datetime.now(),
            contact_type=ContactType.PHYSICAL,
            location="42Madrid",
            signal_strength=8.1,
            duration_minutes=92,
            witness_count=4,
            message_received="E.T Phone Earth",
            is_verified=False
        )
        display_report(invalid_contact)
    except ValidationError as e:
        print_validation_errors(e)


if __name__ == "__main__":
    main()
