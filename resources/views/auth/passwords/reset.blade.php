@extends('layout-auth')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }}
    </div>

    <div class="auth-subtitle">{{ __('Reset Password') }}</div>

    <form method="POST" action="{{ route('password.update') }}">

        @csrf

        <input type="hidden" name="token" value="{{ $token }}">

        <div class="form-group">

            <label for="email">{{ __('E-Mail Address') }}</label>
            <input id="email" type="email" class="form-control @error('email') is-invalid @enderror" name="email" value="{{ $email ?? old('email') }}" required autocomplete="email" autofocus>

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
                {{ __('Reset Password') }}
            </button>
        </div>
        
    </form>

</div>

@endsection
