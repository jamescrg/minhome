@extends('layouts.app')

@section('content')

<div class="auth-card">

    <div class="auth-title">
        {{ config('app.name') }}
    </div>

    <div class="auth-subtitle">{{ __('Verify Your Email Address') }}</div>

    @if (session('resent'))

        <div class="auth-subtitle" role="alert">
            {{ __('A fresh verification link has been sent to your email address.') }}
        </div>

    @endif

    <div class="auth-subtitle">

        {{ __('Before proceeding, please check your email for a verification link.') }}
        {{ __('If you did not receive the email') }},

    </div>

    <form class="d-inline" method="POST" action="{{ route('verification.resend') }}">
        @csrf
        <button type="submit" class="btn btn-default">{{ __('click here to request another') }}</button>.
    </form>

</div>

@endsection
