<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('promotions', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique();
            $table->string('code')->unique();
            $table->text('description')->nullable();
            $table->decimal('discount', 10, 2);
            $table->enum('type', ['percentage', 'fixed'])->default('percentage');
            $table->date('start_date');
            $table->date('end_date');
            $table->integer('min_purchase')->nullable();
            $table->integer('max_discount')->nullable();
            $table->integer('uses_per_customer')->nullable();
            $table->integer('total_uses')->nullable();
            $table->boolean('status')->default(true);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('promotions');
    }
}; 