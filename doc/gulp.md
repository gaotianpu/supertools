#gulp

1. 解决什么问题?
2. 同类解决方案有哪些?
3. 为什么选择这个方案？

## 下载安装
1. 全局安装gulp
$ sudo npm install --global gulp
安装目录：
/usr/local/bin/gulp -> /usr/local/lib/node_modules/gulp/bin/gulp.js
/usr/local/lib/node_modules/gulp

2. 作为项目的开发依赖安装
npm install --save-dev gulp
(不理解为何还要再安装一次,git项目是否要把node_modules忽略掉~)

3. 编写gulpfile.js
4. 运行 gulp

## 常用插件
项目目录中执行：
npm install gulp-minify-css gulp-uglify gulp-concat gulp-rename gulp-jshint --save-dev

1. css压缩 　　
gulp-minify-css

2.	js压缩　　　
gulp-uglify

3.	js合并　　　
gulp-concat　　

由于压缩之前需要对js代码进行代码检测，压缩完成之后需要加上min的后缀，我们还需要安装另外两个插件：
4.	重命名　　   
gulp-rename

5.	js代码检测　 
gulp-jshint　(或gulp-jslint)

6. 其他

