package kaleidoscopesnack.item;

import net.minecraft.world.item.Item;
import net.minecraft.world.food.FoodProperties;

public class CrispyPorkBellyItem extends Item {
	public CrispyPorkBellyItem() {
		super(new Item.Properties().food((new FoodProperties.Builder()).nutrition(8).saturationModifier(0.6f).alwaysEdible().build()));
	}
}