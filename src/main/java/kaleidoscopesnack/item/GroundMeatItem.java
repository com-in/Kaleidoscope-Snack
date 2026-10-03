package kaleidoscopesnack.item;

import net.minecraft.world.item.Item;
import net.minecraft.world.food.FoodProperties;

public class GroundMeatItem extends Item {
	public GroundMeatItem() {
		super(new Item.Properties().food((new FoodProperties.Builder()).nutrition(2).saturationModifier(0.3f).alwaysEdible().build()));
	}
}