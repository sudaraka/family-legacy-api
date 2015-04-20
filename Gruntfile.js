module.exports = function(g) {
    'use strict';

    var _param = g.file.readJSON('grunt-param.json');

    require('load-grunt-tasks')(g);

    g.initConfig({
        param:  _param,
        venv_home: '$HOME/opt/virtualenv/flapi/',

        // {{{ watch
        watch: {
            docs: {
                files: [
                    'src/docs/conf.py',
                    'src/docs/**/*.rst',
                    'src/app/api/**/*.py'
                ],
                tasks: ['shell:build_doc']
            }
        },
        // }}}

        // shell {{{
        shell: {
            build_doc: {
                command: 'npm run doc'
            }
        }
        // }}}

    });

    g.registerTask('default', ['watch']);

};

