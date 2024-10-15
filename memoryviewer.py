import pymem
import struct
import time
import random

# Base address and offsets (example values)
BASE_ADDRESS = 0x8033B0A0  # Update with the correct base address
ROOM_CONNECTIONS_OFFSET = 0x3E0  # Update with the correct offset

# Room exit mapping
ROOM_EXIT_MAP = {
    0x00: "Sacred Realm",
    0x01: "Hyrule",
    0x02: "Death Mountain",
    0x03: "Goron City",
    0x04: "Gerudo Valley",
    0x05: "Hyrule Castle",
    0x06: "Hyrule Castle Town",
    0x07: "Hyrule Field",
    0x08: "Lon Lon Ranch",
    0x09: "Kakariko Village",
    0x0A: "Kokiri Forest",
    0x0B: "Lake Hylia",
    0x0C: "Lost Woods",
    0x0D: "Zora's Domain",
    # Add more mappings as needed
}

# Item placement map
ITEM_PLACEMENT_MAP = {
    "Sacred Realm": ["Master Sword", "Fairy Fountain"],
    "Hyrule": ["Map", "Compass"],
    "Death Mountain": ["Fireproof Shield", "Goron Bracelet"],
    "Goron City": ["Big Bomb Bag", "Goron Tunic"],
    "Gerudo Valley": ["Hookshot", "Gerudo Card"],
    "Hyrule Castle": ["Fairy Fountain", "Zelda's Lullaby"],
    "Hyrule Castle Town": ["Potion Shop", "Bomb Shop"],
    "Hyrule Field": ["Rupees", "Heart Piece"],
    "Lon Lon Ranch": ["Lon Lon Milk", "Epona"],
    "Kakariko Village": ["Graveyard Key", "Cucco"],
    "Kokiri Forest": ["Fairy Slingshot", "Kokiri Sword"],
    "Lake Hylia": ["Fishing Rod", "Lake Hylia Key"],
    "Lost Woods": ["Ocarina of Time", "Mushrooms"],
    "Zora's Domain": ["Zora Tunic", "Zora's Sapphire"],
    # Add more items as needed
}

def read_memory(process, address):
    """Read 4 bytes from the memory address."""
    data = process.read_bytes(address, 4)
    return struct.unpack('<I', data)[0]

def get_room_connections(process):
    """Get room connections for the current room."""
    connections = {}
    for i in range(4):  # Assuming there are 4 exits per room
        room_address = BASE_ADDRESS + ROOM_CONNECTIONS_OFFSET + (i * 4)
        exit_value = read_memory(process, room_address)
        connections[f'Exit {i}'] = ROOM_EXIT_MAP.get(exit_value, "Unknown")
    return connections

def main():
    # Attach to the emulator process
    process_name = "Project64.exe"  # Replace with your emulator's process name
    try:
        process = pymem.Pymem(process_name)
    except Exception as e:
        print(f"Could not attach to process: {e}")
        return

    try:
        while True:
            connections = get_room_connections(process)
            print("Current Room Connections:")
            for exit_name, room in connections.items():
                print(f"{exit_name}: {room}")
            
            # Display item placements based on current room connections
            for room in connections.values():
                items = ITEM_PLACEMENT_MAP.get(room, [])
                print(f"Items in {room}: {', '.join(items) if items else 'None'}")

            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        print("Exiting viewer.")

if __name__ == "__main__":
    main()
