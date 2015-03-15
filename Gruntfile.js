module.exports = function(g) {
    'use strict';

    var _param = g.file.readJSON('grunt-param.json');

    require('load-grunt-tasks')(g);

    g.initConfig({
        param:  _param,
        venv_home: '$HOME/opt/virtualenv/flapi/',

        // shell {{{
        shell: {
            setup: {
                command: [
                    'mkdir -p <%= venv_home %>',
                    'python -m venv <%= venv_home %>',
                    'mkdir -p <%= venv_home %>Scripts/',
                    'touch <%= venv_home %>Scripts/activate_this.py',
                    'source <%= venv_home %>bin/activate',
                    'pip install -Ur requirements/' + g.option('env', 'dev') + '.txt',
                ].join(' && ')
            }
        }
        // }}}

    });

    g.registerTask('default', []);
    g.registerTask('setup', ['shell:setup']);

};

