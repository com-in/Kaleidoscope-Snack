package kaleidoscopesnack.item;

import net.minecraft.world.item.Item;
import net.minecraft.world.food.FoodProperties;

public class SquidItem extends Item {
	public SquidItem() {
		super(new Item.Properties().food((new FoodProperties.Builder()).nutrition(4).saturationModifier(0.3f).alwaysEdible().build()));
	}
}