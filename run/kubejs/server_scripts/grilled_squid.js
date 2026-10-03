ServerEvents.recipes(event => {

    event.custom({
        type: 'kaleidoscope_cookery:pot',

        carrier: {
            item: 'minecraft:bowl'
        },

        ingredients: [
            {
                item: 'kaleidoscope_snack:raw_squid'
            },
            {
                item: 'kaleidoscope_snack:raw_squid'
            },
            {
                item: 'kaleidoscope_snack:raw_squid'
            },
            {
                tag: 'c:crops/chilipepper'
            }
        ],

        result: {
            count: 1,
            id: 'kaleidoscope_snack:grilled_squid'
        }
    });

});