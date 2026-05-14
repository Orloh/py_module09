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


def display_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Non-Operational"
    crew_label = "crew member" if station.crew_size == 1 else "crew members"

    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} {crew_label}")
    print(f"Power: {station.power_level:.1f}%")
    print(f"Oxygen: {station.oxygen_level:.1f}%")
    print(f"Status: {status}")
    print()


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
        display_station(valid_station)

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
        display_station(invalid_station)
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
