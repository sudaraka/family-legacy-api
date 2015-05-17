module.exports = function(g) {
    'use strict';

    require('load-grunt-tasks')(g);

    g.initConfig({

        // {{{ watch
        watch: {
            docs: {
                files: [
                    'src/docs/conf.py',
                    'src/docs/**/*.rst',
                    'src/app/api/**/*.py',
                    '!**/__pycache__/**'
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

