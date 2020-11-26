<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFoldersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('folders', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id');
            $table->string('page', 50);
            $table->string('name', 50);
            $table->tinyInteger('home_column')->nullable($value = true);
            $table->tinyInteger('home_rank')->nullable($value = true);
            $table->tinyInteger('selected')->nullable($value = true);
            $table->tinyInteger('active')->nullable($value = true);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('folders');
    }
}
