<?php
require '../vendor/autoload.php';
define('ROOT_DIR', dirname(__FILE__) . '/..');
require ROOT_DIR . '/private/config.inc';
require ROOT_DIR . '/private/base.inc';


$app = new \Slim\Slim();
$app->config(array(
    'debug' => true,
    'templates.path' => '../private/templates',
    'view' => '\Slim\View',
    ));

$app->group('/register', function () use ($app) {
    $c = new RegisterController($app);
    $app -> get('',function() use($app){ 
        $c->get(); 
    });

    $app -> post('',function() use($app){ 
        $c->get(); 
    });
});

$app->group('/login', function () use ($app) {
    $c = new LoginController($app);
    $app -> get('',function() use($app){ 
        $c->get(); 
    });

    $app -> post('',function() use($app){ 
        $c->get(); 
    });
});


$app -> get('/',function() use($app){ 
    (new IndexController($app))->get(); 
});


$app->run();

?>