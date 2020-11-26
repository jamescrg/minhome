<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFavoritesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('favorites', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id');
            $table->bigInteger('folder_id')->nullable($value = true);
            $table->string('name', 100)->nullable($value = true);
            $table->string('url', 255)->nullable($value = true);
            $table->string('description', 255)->nullable($value = true);
            $table->string('login', 50)->nullable($value = true);
            $table->string('root', 50)->nullable($value = true);
            $table->string('passkey', 50)->nullable($value = true);
            $table->tinyInteger('selected')->nullable($value = true);
            $table->tinyInteger('home_rank')->nullable($value = true);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('favorites');
    }
}
