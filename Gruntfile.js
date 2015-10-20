module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                files: {
                    'mirigata/website/static/js/vendor.js': [
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/materialize/materialize.js'
                    ],
                    'mirigata/website/static/js/app.js': [
                        'frontend/**/*.js'
                    ]
                }
            }
        },

        cssmin: {
            build: {
                files: {
                    'mirigata/website/static/css/style.css': [
                        'bower_components/materialize/dist/css/materialize.css',
                        'frontend/**/*.css'
                    ]
                }
            }
        },

        copy: {
            build: {
                files: [
                    {
                        expand: true,
                        cwd: 'bower_components/materialize/dist/font',
                        src: ['**'],
                        dest: 'mirigata/website/static/font'
                    }
                ]
            }

        },

        watch: {
            options: {
                livereload: true,
                spawn: false
            },
            scripts: {
                files: ['frontend/**/*.js'],
                tasks: ['uglify']
            },
            styles: {
                files: ['frontend/**/*.css'],
                tasks: ['cssmin']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-copy');

    // Default task(s).
    grunt.registerTask('default', ['cssmin', 'uglify', 'copy']);

};
