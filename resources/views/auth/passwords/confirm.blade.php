@extends('layouts.app')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }}
    </div>

    <div class="auth-subtitle">{{ __('Confirm Password') }}</div>

    <div class="auth-subtitle">

        {{ __('Please confirm your password before continuing.') }}

    </div>

    <form method="POST" action="{{ route('password.confirm') }}">

        @csrf

        <div class="form-group">

            <label for="password">{{ __('Password') }}</label>

            <input id="password" type="password" class="form-control @error('password') is-invalid @enderror" name="password" required autocomplete="current-password">

                @error('password')

                    <span class="invalid-feedback" role="alert">
                        <strong>{{ $message }}</strong>
                    </span>

                @enderror
        </div>

        <div class="form-group">

            <button type="submit" class="btn btn-primary">
                {{ __('Confirm Password') }}
            </button>

            @if (Route::has('password.request'))
                <a class="btn btn-link" href="{{ route('password.request') }}">
                    {{ __('Forgot Your Password?') }}
                </a>
            @endif

        </div>

    </form>

</div>

@endsection
