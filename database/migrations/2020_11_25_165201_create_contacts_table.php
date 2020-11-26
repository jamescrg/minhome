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
            $table->tinyInteger('selected')->nullable($value = true);
            $table->string('name', 100);
            $table->string('company', 100)->nullable($value = true);
            $table->string('address', 255)->nullable($value = true);
            $table->string('phone1', 50)->nullable($value = true);
            $table->string('phone1_label', 10)->nullable($value = true);
            $table->string('phone2', 50)->nullable($value = true);
            $table->string('phone2_label', 10)->nullable($value = true);
            $table->string('phone3', 50)->nullable($value = true);
            $table->string('phone3_label', 10)->nullable($value = true);
            $table->string('email', 100)->nullable($value = true);
            $table->string('website', 255)->nullable($value = true);
            $table->string('map', 255)->nullable($value = true);
            $table->string('notes', 255)->nullable($value = true);
            $table->string('google_id', 255)->nullable($value = true);
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
