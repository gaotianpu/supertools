<?php
abstract class BaseDAO {

    protected  $dbR;
    protected  $dbW;

    function __construct() { 
        $this->dbR =  new PDO(Config::$dbRinfo['dsn'],Config::$dbRinfo['username'],Config::$dbRinfo['password']); 
        $this->dbW =  new PDO(Config::$dbWinfo['dsn'],Config::$dbWinfo['username'],Config::$dbWinfo['password']); 
    }
}
?>