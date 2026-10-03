ServerEvents.recipes(event => {

    event.custom({
        type: 'kaleidoscope_cookery:pot',

        carrier: {
            item: 'minecraft:bowl'
        },

        ingredients: [
            {
                tag: 'c:dough'
            },
            {
                tag: 'c:eggs'
            },
            {
                tag: 'c:crops/lettuce'
            },
            {
                tag: 'c:foods/raw_chicken'
            },
            {
                tag: 'c:crops/chilipepper'
            }
        ],

        result: {
            count: 1,
            id: 'kaleidoscope_snack:pancake'
        }
    });

});