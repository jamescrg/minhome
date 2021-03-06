@extends('layout-auth')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }}
    </div>

    <div class="auth-subtitle">
        Log in to your account
    </div>

    <form method="post" action="{{ route('login') }}">

        @csrf

        <div class="form-group">
            <label for="email">{{ __('E-Mail Address') }}</label>
            <input id="email" type="email" class="form-control @error('email') is-invalid @enderror" name="email" value="{{ old('email') }}" required autocomplete="email" autofocus>
            @error('email')<div class="invalid-feedback" role="alert">{{ $message }}</div>@enderror
        </div>

        <div class="form-group">
            <label for="password">{{ __('Password') }}</label>
            <input id="password" type="password" class="form-control @error('password') is-invalid @enderror" name="password" required autocomplete="current-password">
            @error('password')<div class="invalid-feedback" role="alert">{{ $message }}</div>@enderror
        </div>

        <div class="form-group">
                <input type="checkbox" name="remember" id="remember" {{ old('remember') ? 'checked' : '' }}>
                <label class="form-check-label" for="remember">
                    {{ __('Remember Me') }}
                </label>

        </div>
        <div class="form-group">
                <button type="submit" class="btn btn-default">
                    {{ __('Login') }}
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
