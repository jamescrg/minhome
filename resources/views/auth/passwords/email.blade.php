@extends('layout-auth')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }} 
    </div>

    <div class="auth-subtitle">
        {{ __('Reset Password') }}
    </div>

    @if (session('status'))
        <div class="auth-subtitle" role="alert">
            {{ session('status') }}
        </div>
    @endif

    <form method="POST" action="{{ route('password.email') }}">

        @csrf

        <div class="form-group">

        <label for="email">{{ __('E-Mail Address') }}</label>
        <input id="email" type="email" class="form-control @error('email') is-invalid @enderror" name="email" value="{{ old('email') }}" required autocomplete="email" autofocus>

        @error('email')
        <div class="invalid-feedback" role="alert">
        {{ $message }}
        </div>
        @enderror

        </div>

        <div class="form-group">
            <button type="submit" class="btn btn-default">
                {{ __('Send Password Reset Link') }}
            </button>
        </div>

    </form>

</div>

@endsection
