<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateContactsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('contacts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id');
            $table->bigInteger('folder_id');
            $table->tinyInteger('selected');
            $table->string('name', 100);
            $table->string('address', 255);
            $table->string('phone1', 50);
            $table->string('phone1_label', 10);
            $table->string('phone2', 50);
            $table->string('phone2_label', 10);
            $table->string('phone3', 50);
            $table->string('phone3_label', 10);
            $table->string('email', 100);
            $table->string('website', 255);
            $table->string('map', 255);
            $table->string('notes', 255);
            $table->string('google_id', 255);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('contacts');
    }
}
