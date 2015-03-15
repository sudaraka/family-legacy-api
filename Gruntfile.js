module.exports = function(g) {
    'use strict';

    var _param = g.file.readJSON('grunt-param.json');

    require('load-grunt-tasks')(g);

    g.initConfig({
        param:  _param,

    });

    g.registerTask('default', []);

};

