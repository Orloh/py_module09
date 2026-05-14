#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    alien_contact.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/14 16:30:09 by orhernan          #+#    #+#              #
#    Updated: 2026/05/14 16:30:09 by orhernan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

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
    location: str = Field(min_length=3, max_length=15)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact_id(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValidationError("contact_id must contain AC")
        return self

    @model_validator
    def validate_physical_contact(self) -> 'AlienContact':
        ...
    
    @model_validator
    def validate_telepathic_contact(self) -> 'AlienContact':
        ...
    
    @model_validator
    def validate_strong_signal(self) -> 'AlienContact':
        ...
