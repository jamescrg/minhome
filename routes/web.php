<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\FoldersController;
use App\Http\Controllers\FavoritesController;
use App\Http\Controllers\TasksController;
use App\Http\Controllers\ContactsController;
use App\Http\Controllers\NotesController;
use App\Http\Controllers\SettingsController;
use App\Http\Controllers\SearchController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});


Auth::routes();

Route::get('/', [HomeController::class, 'index']);
Route::get('/home', [HomeController::class, 'index'])->name('home');

Route::get('home/favorite/{id}/{direction}', [HomeController::class, 'favorite']);
Route::get('home/folder/{id}/{direction}', [HomeController::class, 'folder']);

Route::get('folders/home/{id}/{page}', [FoldersController::class, 'home']);
Route::get('folders/delete/{id}/{page}', [FoldersController::class, 'destroy']);
Route::get('folders/{id}/{page}', [FoldersController::class, 'select']);
Route::post('folders/create/{page}', [FoldersController::class, 'store']);
Route::post('folders/update/{id}/{page}', [FoldersController::class, 'update']);

Route::get('favorites', [FavoritesController::class, 'index']);
Route::get('favorites/create/{id}', [FavoritesController::class, 'create']);
Route::get('favorites/edit/{id}', [FavoritesController::class, 'edit']);
Route::get('favorites/home/{id}', [FavoritesController::class, 'home']);
Route::get('favorites/delete/{id}', [FavoritesController::class, 'destroy']);
Route::post('favorites', [FavoritesController::class, 'store']);
Route::post('favorites/update/{id}', [FavoritesController::class, 'update']);

Route::get('tasks', [TasksController::class, 'index']);
Route::get('tasks/lists/{id}', [TasksController::class, 'select']);
Route::get('tasks/edit/{id}', [TasksController::class, 'edit']);
Route::get('tasks/activate/{id}', [TasksController::class, 'activate']);
Route::get('tasks/complete/{id}', [TasksController::class, 'status']);
Route::get('tasks/clear/{listId}', [TasksController::class, 'clear']);
Route::post('tasks', [TasksController::class, 'store']);
Route::post('tasks/update/{id}', [TasksController::class, 'update']);
Route::post('tasks/lists/create', [TasksController::class, 'storeList']);
Route::post('tasks/lists/edit/{id}', [TasksController::class, 'updateList']);

Route::get('contacts', [ContactsController::class, 'index']);
Route::get('contacts/create/{id}', [ContactsController::class, 'create']);
Route::get('contacts/edit/{id}', [ContactsController::class, 'edit']);
Route::get('contacts/{id}', [ContactsController::class, 'show']);
Route::post('contacts', [ContactsController::class, 'store']);
Route::post('contacts/update/{id}', [ContactsController::class, 'update']);
Route::get('contacts/delete/{id}', [ContactsController::class, 'destroy']);

Route::get('notes', [NotesController::class, 'index']);
Route::get('notes/create/{id}', [NotesController::class, 'create']);
Route::get('notes/{id}', [NotesController::class, 'show']);
Route::get('notes/edit/{id}', [NotesController::class, 'edit']);
Route::post('notes', [NotesController::class, 'store']);
Route::post('notes/update/{id}', [NotesController::class, 'update']);
Route::get('notes/delete/{id}', [NotesController::class, 'destroy']);

Route::get('settings', [SettingsController::class, 'index']);
Route::get('settings/google/login', [SettingsController::class, 'googleLogin']);
Route::get('settings/google/store', [SettingsController::class, 'googleStore']);
Route::get('settings/google/logout', [SettingsController::class, 'googleLogout']);

Route::get('search', [SearchController::class, 'index']);
Route::post('search', [SearchController::class, 'search']);

