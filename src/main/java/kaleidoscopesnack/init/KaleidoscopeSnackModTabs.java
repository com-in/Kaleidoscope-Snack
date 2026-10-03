/*
 *    MCreator note: This file will be REGENERATED on each build.
 */
package kaleidoscopesnack.init;

import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.DeferredHolder;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.network.chat.Component;
import net.minecraft.core.registries.Registries;

import kaleidoscopesnack.KaleidoscopeSnackMod;

public class KaleidoscopeSnackModTabs {
	public static final DeferredRegister<CreativeModeTab> REGISTRY = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, KaleidoscopeSnackMod.MODID);
	public static final DeferredHolder<CreativeModeTab, CreativeModeTab> KALEIDOSCOPE_SNACK = REGISTRY.register("kaleidoscope_snack",
			() -> CreativeModeTab.builder().title(Component.translatable("item_group.kaleidoscope_snack.kaleidoscope_snack")).icon(() -> new ItemStack(KaleidoscopeSnackModItems.PANCAKE.get())).displayItems((parameters, tabData) -> {
				tabData.accept(KaleidoscopeSnackModItems.PANCAKE.get());
				tabData.accept(KaleidoscopeSnackModItems.GRILLED_SQUID.get());
				tabData.accept(KaleidoscopeSnackModItems.POTSTICKERS.get());
				tabData.accept(KaleidoscopeSnackModItems.COOKED_SAUSAGE.get());
				tabData.accept(KaleidoscopeSnackModItems.SPICY_CRINKLE_CUT_FRIES.get());
				tabData.accept(KaleidoscopeSnackModItems.SAUSAGE.get());
				tabData.accept(KaleidoscopeSnackModItems.SAUSAGE_CASING.get());
				tabData.accept(KaleidoscopeSnackModItems.GROUND_MEAT.get());
				tabData.accept(KaleidoscopeSnackModItems.RAW_SQUID.get());
				tabData.accept(KaleidoscopeSnackModItems.POTATO_CHUNKS.get());
			}).build());
}