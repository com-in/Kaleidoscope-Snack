#!/usr/bin/env node
/**
 * KubeJS 配方 -> 原生数据包配方 转换器
 *
 * 读取  run/kubejs/server_scripts/**.js  中的 KubeJS 配方脚本，
 * 生成  src/main/resources/data/kaleidoscope_snack/recipe/**.json
 *
 * 这样 JAR 里只包含静态的原生配方 JSON，玩家无需安装 KubeJS。
 *
 * 用法: node tools/kubejs-to-datapack.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC_DIR = path.join(ROOT, 'run', 'kubejs', 'server_scripts');
const OUT_DIR = path.join(ROOT, 'src', 'main', 'resources', 'data', 'kaleidoscope_snack', 'recipe');

// ---------------------------------------------------------------- 归一化工具

/** '3x ns:item' -> { id, count } */
function parseItemString(raw) {
  const s = String(raw).trim();
  const m = s.match(/^(\d+)x\s+(.+)$/);
  if (m) return { id: m[2].trim(), count: parseInt(m[1], 10) };
  return { id: s, count: 1 };
}

/** 任意写法 -> ItemStack JSON { id, count } */
function toItemStack(value) {
  if (value && typeof value === 'object') {
    const id = value.id ?? value.item;
    if (id) return { id, count: value.count ?? 1 };
  }
  return parseItemString(value);
}

/** 字符串 -> Ingredient JSON；'#tag' 视为标签 */
function toIngredient(value) {
  if (typeof value === 'string') {
    const s = value.trim();
    return s.startsWith('#') ? { tag: s.slice(1) } : { item: s };
  }
  return value;
}

// ------------------------------------------------------------- KubeJS 运行时桩

let currentSource = '<unknown>';
const captured = [];

function capture(entry) {
  captured.push({ ...entry, source: currentSource });
}

const recipesProxy = new Proxy(
  {},
  {
    get(_t, ns) {
      if (typeof ns !== 'string') return undefined;
      return new Proxy(
        {},
        {
          get(_t2, type) {
            if (typeof type !== 'string') return undefined;
            return (...args) => capture({ kind: 'recipe', ns, type, args });
          },
        },
      );
    },
  },
);

const eventStub = {
  custom: (json) => capture({ kind: 'custom', json }),
  shaped: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'crafting_shaped', args: a }),
  shapeless: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'crafting_shapeless', args: a }),
  smelting: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'smelting', args: a }),
  smoking: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'smoking', args: a }),
  blasting: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'blasting', args: a }),
  campfireCooking: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'campfire_cooking', args: a }),
  stonecutting: (...a) => capture({ kind: 'recipe', ns: 'minecraft', type: 'stonecutting', args: a }),
  recipes: recipesProxy,
};

const serverEventsStub = {
  recipes: (cb) => cb(eventStub),
  tags: () => {},
};

const ItemStub = {
  of(value, count) {
    const stack = toItemStack(value);
    if (count != null) stack.count = count;
    return stack;
  },
};

const consoleStub = { info() {}, log() {}, warn() {}, error() {} };

// ------------------------------------------------------------- JS -> 原生 JSON

function serialize(entry) {
  // event.custom({...}) 已经是原生 JSON，原样输出
  if (entry.kind === 'custom') {
    if (!entry.json || !entry.json.type) {
      throw new Error(`event.custom 缺少 type (来自 ${entry.source})`);
    }
    return { type: entry.json.type, json: entry.json };
  }

  const key = `${entry.ns}:${entry.type}`;
  const a = entry.args;

  switch (key) {
    // 炒锅：event.custom({ type:'kaleidoscope_cookery:pot', ... }) 也是走 custom
    case 'kaleidoscope_cookery:chopping_board':
      // KubeJS 参数顺序: (result, ingredient, model_id, cut_count)
      return {
        type: key,
        json: prune({
          type: key,
          ingredient: toIngredient(a[1]),
          model_id: a[2],
          cut_count: a[3],
          result: toItemStack(a[0]),
        }),
      };

    case 'kaleidoscope_cookery:stockpot':
      // KubeJS 参数顺序: (result, ingredients[], soup_base, carrier)
      return {
        type: key,
        json: prune({
          type: key,
          soup_base: a[2],
          ingredients: (a[1] ?? []).map(toIngredient),
          result: toItemStack(a[0]),
        }),
      };

    case 'minecraft:crafting_shaped':
      // event.shaped(result, pattern[], key{})
      return {
        type: key,
        json: {
          type: key,
          pattern: a[1],
          key: Object.fromEntries(Object.entries(a[2] ?? {}).map(([k, v]) => [k, toIngredient(v)])),
          result: toItemStack(a[0]),
        },
      };

    case 'minecraft:crafting_shapeless':
      return {
        type: key,
        json: {
          type: key,
          ingredients: (a[1] ?? []).map(toIngredient),
          result: toItemStack(a[0]),
        },
      };

    case 'minecraft:campfire_cooking':
    case 'minecraft:smelting':
    case 'minecraft:smoking':
    case 'minecraft:blasting':
      // KubeJS 参数顺序: (result, ingredient, experience, cookingtime)
      return {
        type: key,
        json: prune({
          type: key,
          ingredient: toIngredient(a[1]),
          result: toItemStack(a[0]),
          experience: a[2],
          cookingtime: a[3],
        }),
      };

    case 'minecraft:stonecutting':
      return {
        type: key,
        json: {
          type: key,
          ingredient: toIngredient(a[1]),
          result: toItemStack(a[0]),
        },
      };

    default:
      throw new Error(
        `不支持的配方类型 "${key}" (来自 ${entry.source})。` +
          `请在 tools/kubejs-to-datapack.mjs 中补充该类型的转换规则，或改用 event.custom({...})。`,
      );
  }
}

/** 去掉值为 undefined 的字段 */
function prune(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, v]) => v !== undefined));
}

// ------------------------------------------------------------------- 主流程

function walkJs(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const st = fs.statSync(full);
    if (st.isDirectory()) out.push(...walkJs(full));
    else if (name.toLowerCase().endsWith('.js')) out.push(full);
  }
  return out;
}

function main() {
  if (!fs.existsSync(SRC_DIR)) {
    console.warn(`[skip] 找不到 ${path.relative(ROOT, SRC_DIR)}，保留已提交的配方 JSON。`);
    return;
  }

  const files = walkJs(SRC_DIR).sort();
  for (const file of files) {
    currentSource = path.relative(ROOT, file);
    const code = fs.readFileSync(file, 'utf8');
    try {
      new Function('ServerEvents', 'Item', 'console', code)(serverEventsStub, ItemStub, consoleStub);
    } catch (e) {
      throw new Error(`执行 ${currentSource} 失败: ${e.message}`);
    }
  }

  if (captured.length === 0) {
    console.warn('[warn] 没有从 KubeJS 脚本中解析到任何配方。');
    return;
  }

  // 清空旧的生成结果（整个 recipe/ 目录由本脚本生成）
  fs.mkdirSync(OUT_DIR, { recursive: true });
  for (const f of fs.readdirSync(OUT_DIR)) {
    if (f.endsWith('.json')) fs.rmSync(path.join(OUT_DIR, f));
  }

  // 按源文件名分组，生成稳定且唯一的文件名
  const bySource = new Map();
  for (const entry of captured) {
    const base = path.basename(entry.source).replace(/\.js$/i, '');
    if (!bySource.has(base)) bySource.set(base, []);
    bySource.get(base).push(entry);
  }

  const written = [];
  for (const [base, entries] of bySource) {
    const multi = entries.length > 1;
    entries.forEach((entry, i) => {
      const fileName = multi ? `${base}_${i + 1}.json` : `${base}.json`;
      const { json } = serialize(entry);
      fs.writeFileSync(path.join(OUT_DIR, fileName), JSON.stringify(json, null, 2) + '\n', 'utf8');
      written.push(`${fileName}  <-  ${path.relative(ROOT, entry.source)} (${json.type})`);
    });
  }

  console.log(`已生成 ${written.length} 个原生配方到 ${path.relative(ROOT, OUT_DIR)}:`);
  for (const line of written) console.log('  ' + line);
}

main();