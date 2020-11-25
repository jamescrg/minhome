@extends('layout-auth')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }}
    </div>

    <div class="auth-subtitle">
        {{ __('Register') }} a New Account
    </div>

    <form method="POST" action="{{ route('register') }}">

        @csrf

        <div class="form-group">
            <label for="name">{{ __('Name') }}</label>
            <input id="name" type="text" class="form-control @error('name') is-invalid @enderror" name="name" value="{{ old('name') }}" required autocomplete="name" autofocus>

            @error('name')
            <div class="invalid-feedback" role="alert">
                {{ $message }}
            </div>
            @enderror
        </div>

        <div class="form-group">
            <label for="email">{{ __('E-Mail Address') }}</label>
            <input id="email" type="email" class="form-control @error('email') is-invalid @enderror" name="email" value="{{ old('email') }}" required autocomplete="email">

            @error('email')
            <div class="invalid-feedback" role="alert">
                {{ $message }}
            </div>
            @enderror
        </div>

        <div class="form-group">
            <label for="password">{{ __('Password') }}</label>

            <input id="password" type="password" class="form-control @error('password') is-invalid @enderror" name="password" required autocomplete="new-password">

            @error('password')
            <div class="invalid-feedback" role="alert">
                {{ $message }}
            </div>
            @enderror
        </div>

        <div class="form-group">
            <label for="password-confirm">{{ __('Confirm Password') }}</label>
            <input id="password-confirm" type="password" class="form-control" name="password_confirmation" required autocomplete="new-password">
        </div>

        <div class="form-group">
            <button type="submit" class="btn btn-default">
                {{ __('Register') }}
            </button>
        </div>

    </form>

</div>
         
@endsection
