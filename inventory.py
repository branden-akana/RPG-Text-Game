

class InventoryHolder:
    """An object that can hold an inventory."""

    def __init__(self):

        # the list of items in this inventory
        self.inventory = []

    def has_item(self, name: str):
        """Return if this inventory has an item (by name)."""

        return any([item.name == name for item in self.inventory])

    def give_item(self, *items):
        """Add items to this inventory."""

        self.inventory += items

    def remove_item(self, name: str):
        """Remove an item from this inventory.

        If multiple items with the same name exist, only remove one of them.
        """

        found = False
        for i, item in enumerate(self.inventory):
            if item.name == name:
                del self.inventory[i]
                found = True
                break

        return found

    def describe_inventory(self) -> str:
        """Get a description of this inventory in readable format."""

        lines = ["Inventory:"]

        for item in self.inventory:
            lines += [f"- {item.name}"]

        return '\n'.join(lines)
