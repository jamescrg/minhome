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
            $table->bigInteger('folder_id');
            $table->string('name', 100);
            $table->string('url', 255);
            $table->string('description', 255);
            $table->string('login', 50);
            $table->string('root', 50);
            $table->string('passkey', 50);
            $table->tinyInteger('selected');
            $table->tinyInteger('home_rank');
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
