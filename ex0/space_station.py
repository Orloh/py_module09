#!/usr/bin/env python3
# ************************************************************************** #
#                                                                            #
#                                                       :::      ::::::::    #
#  space_station.py                                   :+:      :+:    :+:    #
#                                                   +:+ +:+         +:+      #
#  By: orhernan <orhernan@student.42.fr>          +#+  +:+       +#+         #
#                                               +#+#+#+#+#+   +#+            #
#  Created: 2026/05/13 16:11:57 by orhernan          #+#    #+#              #
#  Updated: 2026/05/13 16:11:57 by orhernan         ###   ########.fr        #
#                                                                            #
# ************************************************************************** #

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main():
    print("Space Station Data Validation")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.today(),
        )
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")

    except ValidationError as e:
        print(f"Unexpected Error: {e}")

    print("\nExpected validation error:")
    try:
        invalid_station = SpaceStation(
            station_id="ST",
            name="Error Station",
            crew_size=25,
            power_level=150,
            oxygen_level=90,
            last_maintenance=datetime.now()
        )
        print("Invalid station created:")
        print(f"ID: {invalid_station.station_id}")
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
