module.exports = function(grunt) {

    require('load-grunt-tasks')(grunt);

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        dest: 'mirigata/website/static',
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                files: {
                    '<%= dest %>/js/vendor.js': [
                        'bower_components/material-design-lite/material.js'
                    ],
                    '<%= dest %>/js/app.js': [
                        'frontend/**/*.js'
                    ]
                }
            }
        },
        //copy: {
        //    build: {
        //        files: [
        //            {
        //                expand: true,
        //                cwd: 'bower_components/material-design/dist/font',
        //                src: ['**'],
        //                dest: '<%= dest %>/font'
        //            }
        //        ]
        //    }
        //},
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
                files: ['frontend/**/*.scss'],
                tasks: ['sass:watch']
            }
        },

        sass: {
            options: {
                style: 'compressed'
            },
            build: {
                files: {
                    '<%= dest %>/css/style.css': [
                        'frontend/styles/app.scss'
                    ]
                }
            },
            watch: {
                files: {
                    '<%= dest %>/css/style.css': [
                        'frontend/styles/app.scss'
                    ]
                },
                options: {
                    update: true
                }
            }
        }
    });

    // Default task(s).
    grunt.registerTask('default', ['sass:build', 'uglify']);

};
