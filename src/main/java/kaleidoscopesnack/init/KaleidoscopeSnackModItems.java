/*
 *    MCreator note: This file will be REGENERATED on each build.
 */
package kaleidoscopesnack.init;

import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredItem;

import net.minecraft.world.item.Item;

import kaleidoscopesnack.item.*;

import kaleidoscopesnack.KaleidoscopeSnackMod;

public class KaleidoscopeSnackModItems {
	public static final DeferredRegister.Items REGISTRY = DeferredRegister.createItems(KaleidoscopeSnackMod.MODID);
	public static final DeferredItem<Item> PANCAKE;
	public static final DeferredItem<Item> RAW_SQUID;
	public static final DeferredItem<Item> GRILLED_SQUID;
	public static final DeferredItem<Item> POTSTICKERS;
	public static final DeferredItem<Item> GROUND_MEAT;
	public static final DeferredItem<Item> SAUSAGE;
	public static final DeferredItem<Item> SAUSAGE_CASING;
	public static final DeferredItem<Item> COOKED_SAUSAGE;
	public static final DeferredItem<Item> POTATO_CHUNKS;
	public static final DeferredItem<Item> SPICY_CRINKLE_CUT_FRIES;
	static {
		PANCAKE = REGISTRY.register("pancake", JianbingItem::new);
		RAW_SQUID = REGISTRY.register("raw_squid", SquidItem::new);
		GRILLED_SQUID = REGISTRY.register("grilled_squid", GrilledSquidItem::new);
		POTSTICKERS = REGISTRY.register("potstickers", PotstickersItem::new);
		GROUND_MEAT = REGISTRY.register("ground_meat", GroundMeatItem::new);
		SAUSAGE = REGISTRY.register("sausage", SausageItem::new);
		SAUSAGE_CASING = REGISTRY.register("sausage_casing", SausageCasingItem::new);
		COOKED_SAUSAGE = REGISTRY.register("cooked_sausage", CookedSausageItem::new);
		POTATO_CHUNKS = REGISTRY.register("potato_chunks", PotatoChunksItem::new);
		SPICY_CRINKLE_CUT_FRIES = REGISTRY.register("spicy_crinkle_cut_fries", SpicyCrinkleCutFriesItem::new);
	}
	// Start of user code block custom items
	// End of user code block custom items
}