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
            setup: {
                command: [
                    'mkdir -p <%= venv_home %>',
                    'python -m venv <%= venv_home %>',
                    'mkdir -p <%= venv_home %>Scripts/',
                    'touch <%= venv_home %>Scripts/activate_this.py',
                    'source <%= venv_home %>bin/activate',
                    'pip install -Ur requirements/' + g.option('env', 'development') + '.txt',
                ].join(' && ')
            },

            build_doc: {
                command: 'sphinx-build -b html src/docs src/docs/_build'
            }
        }
        // }}}

    });

    g.registerTask('default', ['watch']);
    g.registerTask('setup', ['shell:setup']);
    g.registerTask('doc', ['shell:build_doc']);

};

