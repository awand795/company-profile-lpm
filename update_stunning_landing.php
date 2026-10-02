<?php
require_once('/var/www/html/wp-load.php');

$page_id = 13; // Beranda page ID

$html = <<<'HTML'
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MASTER TRUCK - Bengkel Perawatan & Perbaikan Truk dan Armada Niaga</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    html {
      scroll-behavior: smooth;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #080E1A;
      color: #F8FAFC;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    /* Container */
    .container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 24px;
    }

    /* Top Sticky Navbar */
    .site-nav {
      position: sticky;
      top: 0;
      z-index: 999;
      background: rgba(8, 14, 26, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding: 14px 0;
      transition: all 0.3s ease;
    }
    .nav-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }
    .brand-box {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }
    .brand-logo {
      height: 40px;
      width: auto;
      object-contain: contain;
    }
    .brand-text h1 {
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #FFFFFF;
      line-height: 1.2;
    }
    .brand-text span {
      font-size: 10px;
      color: #2DD4BF;
      font-weight: 600;
      letter-spacing: 0.3px;
      display: block;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 28px;
      list-style: none;
    }
    .nav-links a {
      color: #94A3B8;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: color 0.2s;
    }
    .nav-links a:hover {
      color: #2DD4BF;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn-login {
      background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
      color: #FFFFFF !important;
      padding: 9px 20px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      box-shadow: 0 2px 10px rgba(20, 184, 166, 0.35);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .btn-login:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(20, 184, 166, 0.5);
    }
    .btn-register {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #FFFFFF !important;
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .btn-register:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: #2DD4BF;
      color: #2DD4BF !important;
    }

    /* Hero Section */
    .hero {
      position: relative;
      padding: 110px 0 100px 0;
      background: linear-gradient(170deg, rgba(8, 14, 26, 0.82) 0%, rgba(8, 14, 26, 0.95) 100%),
                  url('https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
      overflow: hidden;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(20, 184, 166, 0.12);
      border: 1px solid rgba(20, 184, 166, 0.4);
      padding: 6px 16px;
      border-radius: 9999px;
      margin-bottom: 24px;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #2DD4BF;
      box-shadow: 0 0 12px #2DD4BF;
    }
    .hero-badge span {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: #5EEAD4;
      text-transform: uppercase;
    }
    .hero-title {
      font-size: 48px;
      line-height: 1.15;
      font-weight: 800;
      letter-spacing: -0.8px;
      color: #FFFFFF;
      max-width: 900px;
      margin-bottom: 20px;
    }
    .text-gradient {
      background: linear-gradient(135deg, #2DD4BF 0%, #38BDF8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-desc {
      font-size: 17px;
      line-height: 1.65;
      color: #94A3B8;
      max-width: 720px;
      margin-bottom: 36px;
    }
    .hero-cta {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      margin-bottom: 60px;
    }
    .btn-hero-primary {
      background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
      color: #FFFFFF;
      padding: 15px 32px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 15px;
      text-decoration: none;
      box-shadow: 0 4px 18px rgba(13, 148, 136, 0.45);
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .btn-hero-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(13, 148, 136, 0.6);
    }
    .btn-hero-secondary {
      background: rgba(255, 255, 255, 0.06);
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      color: #FFFFFF;
      padding: 15px 30px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 15px;
      text-decoration: none;
      backdrop-filter: blur(10px);
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }
    .btn-hero-secondary:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: #2DD4BF;
      color: #2DD4BF;
    }

    /* Stats Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(51, 65, 85, 0.8);
      border-radius: 14px;
      padding: 24px 30px;
      backdrop-filter: blur(12px);
    }
    .stat-item {
      padding-right: 18px;
    }
    .stat-item:not(:last-child) {
      border-right: 1px solid rgba(51, 65, 85, 0.6);
    }
    .stat-num {
      font-size: 34px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #2DD4BF;
      line-height: 1.1;
    }
    .stat-num.blue { color: #38BDF8; }
    .stat-num.amber { color: #F59E0B; }
    .stat-num.emerald { color: #10B981; }
    .stat-label {
      font-size: 13px;
      color: #94A3B8;
      margin-top: 6px;
      font-weight: 500;
    }

    /* Section Styles */
    .section {
      padding: 90px 0;
    }
    .section-light {
      background: #F8FAFC;
      color: #0F172A;
    }
    .section-dark {
      background: #0B1322;
      color: #FFFFFF;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .section-header {
      text-align: center;
      max-width: 760px;
      margin: 0 auto 55px auto;
    }
    .section-eyebrow {
      color: #0D9488;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 2px;
      display: block;
      margin-bottom: 10px;
    }
    .section-title {
      font-size: 36px;
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.6px;
      margin-bottom: 16px;
    }
    .section-desc {
      font-size: 16px;
      line-height: 1.65;
      color: #64748B;
    }
    .section-dark .section-desc {
      color: #94A3B8;
    }

    /* Profile / History Split */
    .profile-split {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 50px;
      align-items: center;
    }
    .profile-img-wrap {
      position: relative;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    .profile-img {
      width: 100%;
      height: 480px;
      object-fit: cover;
      display: block;
    }
    .profile-badge-overlay {
      position: absolute;
      bottom: 24px;
      left: 24px;
      background: rgba(8, 14, 26, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      padding: 16px 20px;
      color: #FFFFFF;
      max-width: 280px;
    }
    .profile-badge-overlay strong {
      display: block;
      font-size: 18px;
      color: #2DD4BF;
      font-family: 'JetBrains Mono', monospace;
    }
    .profile-badge-overlay span {
      font-size: 12px;
      color: #CBD5E1;
    }
    .profile-text-content h3 {
      font-size: 26px;
      font-weight: 800;
      color: #0F172A;
      margin-bottom: 18px;
      line-height: 1.3;
    }
    .profile-text-content p {
      font-size: 15px;
      line-height: 1.75;
      color: #475569;
      margin-bottom: 18px;
    }
    .value-cards {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 24px;
    }
    .value-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 18px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .value-card strong {
      display: block;
      font-size: 14px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 6px;
    }
    .value-card p {
      font-size: 12px !important;
      line-height: 1.6 !important;
      color: #64748B !important;
      margin: 0 !important;
    }

    /* Product Cards Grid */
    .products-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 28px;
    }
    .product-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      transition: all 0.25s ease;
    }
    .product-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
      border-color: #CBD5E1;
    }
    .product-img-wrap {
      height: 190px;
      overflow: hidden;
      position: relative;
    }
    .product-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }
    .product-card:hover .product-img {
      transform: scale(1.05);
    }
    .product-cat-tag {
      position: absolute;
      top: 14px;
      left: 14px;
      background: rgba(8, 14, 26, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #2DD4BF;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 6px;
    }
    .product-body {
      padding: 22px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
    }
    .product-title {
      font-size: 18px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 8px;
    }
    .product-desc {
      font-size: 13px;
      line-height: 1.6;
      color: #64748B;
      margin-bottom: 18px;
    }
    .product-brands {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 10px 14px;
    }
    .product-brands span {
      font-size: 10px;
      color: #94A3B8;
      font-weight: 700;
      text-transform: uppercase;
      display: block;
      margin-bottom: 2px;
    }
    .product-brands strong {
      font-size: 13px;
      font-weight: 700;
      color: #0F172A;
    }

    /* Fleet Integration Banner */
    .fleet-banner {
      background: linear-gradient(135deg, #090D16 0%, #111C2E 100%);
      border: 1px solid rgba(20, 184, 166, 0.3);
      border-radius: 18px;
      padding: 50px 40px;
      position: relative;
      overflow: hidden;
    }
    .fleet-inner {
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 40px;
      align-items: center;
    }
    .fleet-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(45, 212, 191, 0.12);
      border: 1px solid rgba(45, 212, 191, 0.4);
      padding: 4px 14px;
      border-radius: 9999px;
      color: #5EEAD4;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 16px;
    }
    .fleet-title {
      font-size: 32px;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.25;
      margin-bottom: 16px;
    }
    .fleet-desc {
      font-size: 15px;
      color: #94A3B8;
      line-height: 1.7;
      margin-bottom: 24px;
    }
    .fleet-check-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 32px;
    }
    .fleet-check-item {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      color: #E2E8F0;
    }
    .check-icon {
      color: #2DD4BF;
      font-weight: 800;
    }
    .fleet-mockup {
      background: #060A12;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 14px 40px rgba(0, 0, 0, 0.6);
    }
    .mockup-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #1E293B;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }
    .dots {
      display: flex;
      gap: 6px;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .dot.red { background: #EF4444; }
    .dot.yellow { background: #F59E0B; }
    .dot.green { background: #10B981; }
    .mockup-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #64748B;
    }
    .mockup-card {
      background: #111A29;
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 10px;
      border-left: 3px solid #2DD4BF;
    }
    .mockup-card.blue { border-left-color: #38BDF8; }
    .mockup-card.green { border-left-color: #10B981; }
    .mockup-card strong {
      display: block;
      font-size: 12px;
      color: #FFFFFF;
    }
    .mockup-card span {
      font-size: 11px;
      color: #94A3B8;
    }

    /* Hub & Locations */
    .hub-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 30px;
    }
    .hub-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 14px;
      padding: 32px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
    }
    .hub-icon {
      font-size: 28px;
      margin-bottom: 12px;
      display: block;
    }
    .hub-card h3 {
      font-size: 20px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 12px;
    }
    .hub-card p {
      font-size: 14px;
      line-height: 1.7;
      color: #475569;
      margin-bottom: 16px;
    }
    .region-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 6px;
    }
    .region-badge.sumbagut { background: #E0F2FE; color: #0284C7; }
    .region-badge.sumbagsel { background: #CCFBF1; color: #0F766E; }

    /* Footer */
    .site-footer {
      background: #040810;
      color: #94A3B8;
      padding: 60px 0 30px 0;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .footer-top {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      margin-bottom: 40px;
    }
    .footer-brand h4 {
      font-size: 16px;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 4px;
    }
    .footer-brand p {
      font-size: 12px;
      color: #64748B;
    }
    .footer-links {
      display: flex;
      gap: 24px;
      list-style: none;
    }
    .footer-links a {
      color: #2DD4BF;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      transition: color 0.2s;
    }
    .footer-links a:hover {
      color: #5EEAD4;
      text-decoration: underline;
    }
    .footer-bottom {
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 24px;
      text-align: center;
      font-size: 12px;
      color: #475569;
    }

    /* Responsive */
    @media (max-width: 900px) {
      .hero-title { font-size: 34px; }
      .profile-split { grid-template-columns: 1fr; }
      .fleet-inner { grid-template-columns: 1fr; }
      .nav-links { display: none; }
      .stats-grid { grid-template-columns: 1fr 1fr; }
      .stat-item:not(:last-child) { border-right: none; }
    }
    @media (max-width: 600px) {
      .hero-title { font-size: 28px; }
      .stats-grid { grid-template-columns: 1fr; }
      .brand-text span { display: none; }
    }
  </style>
</head>
<body>

  <!-- STICKY NAVBAR -->
  <header class="site-nav">
    <div class="container nav-inner">
      <a href="#" class="brand-box">
        <img src="/wp-content/uploads/2026/10/logo.png" alt="MASTER TRUCK" class="brand-logo" onerror="this.style.display='none'">
        <div class="brand-text">
          <h1>MASTER TRUCK</h1>
          <span>DISTRIBUTOR OTOMOTIF & PELUMAS NASIONAL</span>
        </div>
      </a>

      <ul class="nav-links">
        <li><a href="#">Beranda</a></li>
        <li><a href="#profil">Profil & Sejarah</a></li>
        <li><a href="#produk">Produk Resmi</a></li>
        <li><a href="#fleet">Web Fleet</a></li>
        <li><a href="#kontak">Kontak & Hub</a></li>
      </ul>

      <div class="nav-actions">
        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-login">
          <span>Login Web Fleet</span>
          <span>&rarr;</span>
        </a>
        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-register">
          <span>Daftar Mitra</span>
        </a>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="hero">
    <div class="container">
      
      <div class="hero-badge">
        <div class="pulse-dot"></div>
        <span>DISTRIBUTOR NASIONAL RESMI • EST. 2000</span>
      </div>

      <h1 class="hero-title">
        Solusi Rantai Pasok Otomotif & <br>
        <span class="text-gradient">Portal Manajemen Armada Fleet Terpadu</span>
      </h1>

      <p class="hero-desc">
        MASTER TRUCK telah lebih dari <strong>24 tahun</strong> menjadi distributor resmi terpercaya oli, aki, ban, dan suku cadang untuk ribuan jaringan bengkel serta armada komersial di seluruh Pulau Sumatera.
      </p>

      <div class="hero-cta">
        <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-hero-primary">
          <span>🔐 Masuk Portal Web Fleet</span>
          <span>&rarr;</span>
        </a>
        <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-hero-secondary">
          <span>📝 Registrasi Mitra Armada</span>
        </a>
      </div>

      <!-- Stats Bar -->
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-num">24+ Th</div>
          <div class="stat-label">Pengalaman Industri (Est. 2000)</div>
        </div>
        <div class="stat-item">
          <div class="stat-num blue">2 Region</div>
          <div class="stat-label">Cakupan SUMBAGUT & SUMBAGSEL</div>
        </div>
        <div class="stat-item">
          <div class="stat-num amber">100% Ori</div>
          <div class="stat-label">Garansi Resmi Pabrikan OEM</div>
        </div>
        <div class="stat-item">
          <div class="stat-num emerald">Ribuan</div>
          <div class="stat-label">Unit Armada & Bengkel Mitra Terlayani</div>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 1: PROFIL & SEJARAH PERUSAHAAN -->
  <section id="profil" class="section section-light">
    <div class="container">
      
      <div class="section-header">
        <span class="section-eyebrow">TENTANG KAMI</span>
        <h2 class="section-title">Profil & Rekam Jejak Perusahaan</h2>
        <p class="section-desc">
          Komitmen konsisten menghadirkan komponen berkualitas tinggi dan distribusi handal demi efisiensi operasional armada mitra bisnis.
        </p>
      </div>

      <div class="profile-split">
        <div class="profile-img-wrap">
          <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1600&q=80" alt="Gudang Distribusi MASTER TRUCK" class="profile-img">
          <div class="profile-badge-overlay">
            <strong>24+ Tahun</strong>
            <span>Menjadi mitra distribusi terpercaya sejak tahun 2000.</span>
          </div>
        </div>

        <div class="profile-text-content">
          <span style="font-size: 11px; font-weight: 700; color: #0284C7; text-transform: uppercase; letter-spacing: 1px;">SEJARAH EST. 2000</span>
          <h3>Dari Spesialisasi Federal Oil Hingga Distributor Terkemuka Sumatera</h3>
          
          <p>
            MASTER TRUCK didirikan pada tahun 2000 berawal dari inisiatif untuk memfokuskan jalur distribusi pelumas terkemuka <strong>Federal Oil</strong> di wilayah Sumatera Utara (Sumut).
          </p>
          <p>
            Berkat konsistensi mutu dan keandalan operasional, perusahaan tumbuh pesat memperluas lini produk ke sektor aki, ban, dan suku cadang mesin, serta mengekspansi jaringan logistik mencakup <strong>SUMBAGUT</strong> (Medan, Aceh, Pekanbaru) dan <strong>SUMBAGSEL</strong> (Palembang, Lampung, Jambi, Bengkulu, Babel).
          </p>

          <div class="value-cards">
            <div class="value-card">
              <strong>Jaminan 100% Produk OEM</strong>
              <p>Dipasok langsung dari prinsipal resmi pabrikan tanpa perantara.</p>
            </div>
            <div class="value-card">
              <strong>Kecepatan Distribusi</strong>
              <p>Hub pergudangan strategis memastikan unit armada Anda tidak tertunda.</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 2: PRODUK RESMI (KATALOG DISTRIBUSI) -->
  <section id="produk" class="section section-dark">
    <div class="container">
      
      <div class="section-header">
        <span class="section-eyebrow" style="color: #2DD4BF;">KATALOG RESMI</span>
        <h2 class="section-title">Produk & Komponen yang Didistribusikan</h2>
        <p class="section-desc">
          Komponen pilihan berstandar internasional untuk kendaraan roda dua, roda empat, armada komersial, dan sektor industri.
        </p>
      </div>

      <div class="products-grid">
        
        <!-- Product 1: Oli -->
        <div class="product-card">
          <div class="product-img-wrap">
            <img src="https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?auto=format&fit=crop&w=800&q=80" alt="Pelumas & Oli Mesin" class="product-img">
            <span class="product-cat-tag">Pelumas</span>
          </div>
          <div class="product-body">
            <div>
              <h3 class="product-title">Oli Mesin & Transmisi</h3>
              <p class="product-desc">
                Pelumas bermutu tinggi dengan formulasi perlindungan gesekan mesin dan efisiensi konsumsi bahan bakar.
              </p>
            </div>
            <div class="product-brands">
              <span>MEREK RESMI:</span>
              <strong>Federal Oil</strong>
            </div>
          </div>
        </div>

        <!-- Product 2: Aki -->
        <div class="product-card">
          <div class="product-img-wrap">
            <img src="https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80" alt="Aki & Baterai Kendaraan" class="product-img">
            <span class="product-cat-tag">Elektrikal</span>
          </div>
          <div class="product-body">
            <div>
              <h3 class="product-title">Aki & Baterai Kendaraan</h3>
              <p class="product-desc">
                Aki Maintenance Free (MF) & aki basah berteknologi Jepang dengan daya starter tinggi di segala kondisi operasional.
              </p>
            </div>
            <div class="product-brands">
              <span>MEREK RESMI:</span>
              <strong>Furukawa Battery (FB)</strong>
            </div>
          </div>
        </div>

        <!-- Product 3: Ban -->
        <div class="product-card">
          <div class="product-img-wrap">
            <img src="https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80" alt="Ban Motor & Truk" class="product-img">
            <span class="product-cat-tag">Roda & Ban</span>
          </div>
          <div class="product-body">
            <div>
              <h3 class="product-title">Ban Motor, Mobil & Truk</h3>
              <p class="product-desc">
                Daya tahan jarak tempuh ekstra, traksi optimal di jalan basah dan kering, serta efisiensi biaya operasional armada.
              </p>
            </div>
            <div class="product-brands">
              <span>MEREK RESMI:</span>
              <strong>Michelin • Indotube • Kaizen</strong>
            </div>
          </div>
        </div>

        <!-- Product 4: Sparepart -->
        <div class="product-card">
          <div class="product-img-wrap">
            <img src="https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=800&q=80" alt="Sparepart OEM" class="product-img">
            <span class="product-cat-tag">Suku Cadang</span>
          </div>
          <div class="product-body">
            <div>
              <h3 class="product-title">Sparepart Mesin & Lampu OEM</h3>
              <p class="product-desc">
                Piston kit, kampas rem, suspensi/shock absorber, dan sistem pencahayaan halogen serta LED otomotif internasional.
              </p>
            </div>
            <div class="product-brands">
              <span>MEREK RESMI:</span>
              <strong>RKN • Ichidai • Sachs • Philips • Osram</strong>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 3: INTEGRASI WEB FLEET -->
  <section id="fleet" class="section section-dark" style="background: #080E1A;">
    <div class="container">
      
      <div class="fleet-banner">
        <div class="fleet-inner">
          <div>
            <div class="fleet-badge">PORTAL DIGITAL FLEET CUSTOMER</div>
            <h2 class="fleet-title">Terkoneksi Langsung dengan Sistem Web Fleet Bengkel</h2>
            <p class="fleet-desc">
              Mitra pelanggan perusahaan dan pemilik armada perorangan dapat memantau seluruh proses servis kendaraan, persetujuan estimasi biaya, alur mekanik, dan suku cadang secara real-time.
            </p>

            <div class="fleet-check-list">
              <div class="fleet-check-item">
                <span class="check-icon">✔</span>
                <span>Lacak status alur servis 5 tahap (Check-in, Inspeksi SA, Mekanik, QC Final, Pass Keluar).</span>
              </div>
              <div class="fleet-check-item">
                <span class="check-icon">✔</span>
                <span>Validasi penawaran estimasi dan rekapitulasi invoice digital terpusat.</span>
              </div>
              <div class="fleet-check-item">
                <span class="check-icon">✔</span>
                <span>Jaminan ketersediaan suku cadang resmi langsung dari MASTER TRUCK.</span>
              </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 14px;">
              <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" class="btn-login" style="padding: 12px 26px; font-size: 14px;">
                <span>Masuk ke Web Fleet</span>
                <span>&rarr;</span>
              </a>
              <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" class="btn-register" style="padding: 12px 24px; font-size: 14px;">
                <span>Daftar Mitra Fleet</span>
              </a>
            </div>
          </div>

          <div class="fleet-mockup">
            <div class="mockup-header">
              <div class="dots">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
              </div>
              <span class="mockup-title">fleet.lotuspradipta.co.id</span>
            </div>
            <div>
              <div class="mockup-card">
                <strong>Unit BK 8821 XA - Hino 500 Tronton</strong>
                <span>Status: Pengerjaan Mekanik • Ganti Kampas Rem RKN & Oli Federal</span>
              </div>
              <div class="mockup-card blue">
                <strong>Unit BG 9021 LP - Isuzu Giga Box</strong>
                <span>Status: QC Final & Uji Jalan • Lolos Inspeksi Foreman</span>
              </div>
              <div class="mockup-card green">
                <strong>Unit BL 4120 MM - Mitsubishi L300</strong>
                <span>Status: Selesai Servis • Gate Out Pass Siap Keluar</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 4: HUB KANTOR UTAMA & WILAYAH OPERASIONAL -->
  <section id="kontak" class="section section-light">
    <div class="container">
      
      <div class="section-header">
        <span class="section-eyebrow">JARINGAN OPERASIONAL</span>
        <h2 class="section-title">Kantor Utama & Hub Distribusi Regional</h2>
        <p class="section-desc">
          Pusat logistik dan pergudangan terpadu untuk memastikan pasokan suku cadang selalu tersedia dan tepat waktu.
        </p>
      </div>

      <div class="hub-grid">
        <div class="hub-card">
          <span class="hub-icon">📍</span>
          <h3>Kantor & Workshop Utama KIM 3 Medan</h3>
          <p>
            <strong>Komplek Pergudangan Palembang Star 1, Blok E5</strong><br>
            Jl. Pulau Bunaken Komplek Warehouse KIM III No. 3A, Mabar, Kec. Medan Labuhan, Kota Medan, Sumatera Utara 20242.
          </p>
          <div style="font-size: 12px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 12px;">
            <strong>Legalitas:</strong> Terdaftar Resmi di Kementerian Perdagangan RI.
          </div>
        </div>

        <div class="hub-card">
          <span class="hub-icon">🌐</span>
          <h3>Jangkauan Distribusi Sumatera</h3>
          
          <div style="margin-bottom: 16px;">
            <span class="region-badge sumbagut">REGION SUMBAGUT</span>
            <p style="margin: 0; font-size: 13px;">Medan (Sumatera Utara), Aceh, dan Pekanbaru (Riau).</p>
          </div>

          <div>
            <span class="region-badge sumbagsel">REGION SUMBAGSEL</span>
            <p style="margin: 0; font-size: 13px;">Kawasan Industri Medan (KIM I, II, III), Belawan, Deli Serdang, dan sekitarnya.</p>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <h4>MASTER TRUCK</h4>
          <p>Distributor Nasional Resmi Pelumas, Aki, Ban & Suku Cadang Otomotif</p>
        </div>
        <ul class="footer-links">
          <li><a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer">Login Web Fleet</a></li>
          <li><a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer">Daftar Mitra Fleet</a></li>
          <li><a href="#profil">Tentang Kami</a></li>
          <li><a href="#produk">Produk Resmi</a></li>
        </ul>
      </div>
      <div class="footer-bottom">
        &copy; 2026 MASTER TRUCK. Seluruh Hak Cipta Dilindungi Undang-Undang. Terdaftar Resmi di Kemendag RI.
      </div>
    </div>
  </footer>

</body>
</html>
HTML;

// Update page
$page_data = [
    'ID'            => $page_id,
    'post_content'  => $html,
    'post_status'   => 'publish',
    'post_type'     => 'page',
];
wp_update_post($page_data);

// Configure Elementor template to full canvas
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_template_type', 'wp-page');

// Also update Astra page meta for full width without sidebar or title
update_post_meta($page_id, 'site-content-layout', 'plain-container');
update_post_meta($page_id, 'site-sidebar-layout', 'no-sidebar');
update_post_meta($page_id, 'ast-title-bar-display', 'disabled');
update_post_meta($page_id, 'ast-featured-img', 'disabled');

echo "Landing page upgraded with state-of-the-art enterprise design!\n";
