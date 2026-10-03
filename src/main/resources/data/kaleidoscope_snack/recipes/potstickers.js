ServerEvents.recipes(event => {

    event.custom({
        type: 'kaleidoscope_cookery:pot',

        carrier: {
            item: 'minecraft:bowl'
        },

        ingredients: [
            {
                item: 'kaleidoscope_cookery:dumpling'
            },
            {
                item: 'kaleidoscope_cookery:dumpling'
            },
            {
                item: 'kaleidoscope_cookery:dumpling'
            }
        ],

        result: {
            count: 1,
            id: 'kaleidoscope_snack:potstickers'
        }
    });

});