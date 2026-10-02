<?php
require_once('/var/www/html/wp-load.php');

// 1. Cek apakah halaman Beranda sudah ada
$existing_page = get_page_by_path('beranda');

$page_content = <<<'HTML'
<!-- HERO SECTION -->
<div style="background: linear-gradient(135deg, #0A1128 0%, #101F42 50%, #0D2B45 100%); color: #ffffff; padding: 90px 24px; position: relative; overflow: hidden; border-bottom: 3px solid #14B8A6;">
  <div style="max-width: 1200px; margin: 0 auto; position: relative; z-index: 2;">
    
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(20, 184, 166, 0.15); border: 1px solid rgba(20, 184, 166, 0.4); padding: 6px 16px; rounded: 50px; border-radius: 50px; margin-bottom: 24px;">
      <span style="display: inline-block; width: 8px; height: 8px; background: #2DD4BF; border-radius: 50%; box-shadow: 0 0 10px #2DD4BF;"></span>
      <span style="font-size: 12px; font-weight: 700; letter-spacing: 1.5px; color: #5EEAD4; text-transform: uppercase;">Bengkel Perawatan & Perbaikan Truk dan Armada Niaga</span>
    </div>

    <h1 style="font-size: 46px; line-height: 1.2; font-weight: 800; margin: 0 0 20px 0; color: #FFFFFF; letter-spacing: -0.5px;">
      Solusi Distribusi Komponen & <br><span style="color: #2DD4BF; background: -webkit-linear-gradient(45deg, #2DD4BF, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Manajemen Armada Fleet Terpadu</span>
    </h1>

    <p style="font-size: 18px; line-height: 1.6; color: #CBD5E1; max-width: 780px; margin: 0 0 36px 0;">
      MASTER TRUCK telah lebih dari <strong>24 tahun</strong> (Est. 2000) menjadi distributor resmi terpercaya pelumas, aki, ban, dan suku cadang untuk ribuan jaringan bengkel serta armada komersial di seluruh Pulau Sumatera.
    </p>

    <!-- ACTION BUTTONS -->
    <div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 50px;">
      <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 10px; background: #0D9488; background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%); color: #FFFFFF; font-weight: 700; font-size: 15px; padding: 15px 30px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 14px rgba(13, 148, 136, 0.4); transition: transform 0.2s;">
        <span>🔐 Masuk Portal Web Fleet</span>
        <span>&rarr;</span>
      </a>

      <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 10px; background: rgba(255, 255, 255, 0.08); border: 1.5px solid rgba(255, 255, 255, 0.25); color: #FFFFFF; font-weight: 700; font-size: 15px; padding: 15px 30px; border-radius: 8px; text-decoration: none; backdrop-filter: blur(10px); transition: background 0.2s;">
        <span>📝 Registrasi Mitra Armada</span>
      </a>
    </div>

    <!-- HIGHLIGHT STATS BAR -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(51, 65, 85, 0.8); border-radius: 12px; padding: 24px; backdrop-filter: blur(10px);">
      <div style="border-right: 1px solid rgba(51, 65, 85, 0.8); padding-right: 16px;">
        <div style="font-size: 32px; font-weight: 800; color: #2DD4BF; font-family: monospace;">24+ Th</div>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Pengalaman Industri (Est. 2000)</div>
      </div>
      <div style="border-right: 1px solid rgba(51, 65, 85, 0.8); padding-right: 16px;">
        <div style="font-size: 32px; font-weight: 800; color: #38BDF8; font-family: monospace;">2 Region</div>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Cakupan SUMBAGUT & SUMBAGSEL</div>
      </div>
      <div style="border-right: 1px solid rgba(51, 65, 85, 0.8); padding-right: 16px;">
        <div style="font-size: 32px; font-weight: 800; color: #F59E0B; font-family: monospace;">100% Ori</div>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Jaminan Asli Pabrikan OEM</div>
      </div>
      <div>
        <div style="font-size: 32px; font-weight: 800; color: #10B981; font-family: monospace;">Ribuan</div>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Armada & Bengkel Mitra Terlayani</div>
      </div>
    </div>

  </div>
</div>

<!-- SECTION 1: PROFIL & SEJARAH PERUSAHAAN -->
<section id="profil" style="padding: 80px 24px; background: #FFFFFF; color: #0F172A;">
  <div style="max-width: 1200px; margin: 0 auto;">
    
    <div style="text-align: center; max-width: 760px; margin: 0 auto 50px auto;">
      <span style="color: #0D9488; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 8px;">TENTANG KAMI</span>
      <h2 style="font-size: 34px; font-weight: 800; color: #0F172A; margin: 0 0 16px 0; letter-spacing: -0.5px;">Profil & Rekam Jejak Perusahaan</h2>
      <p style="font-size: 16px; color: #475569; line-height: 1.6;">
        Komitmen konsisten dalam menghadirkan suku cadang berkualitas tinggi dan distribusi yang handal demi efisiensi operasional mitra bisnis kami.
      </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; align-items: stretch;">
      
      <!-- Card Sejarah -->
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 32px; position: relative;">
        <div style="display: inline-block; background: #E0F2FE; color: #0284C7; font-weight: 700; font-size: 12px; padding: 4px 12px; border-radius: 6px; margin-bottom: 16px;">
          SEJARAH BERDIRI • EST. 2000
        </div>
        <h3 style="font-size: 20px; font-weight: 700; color: #0F172A; margin: 0 0 14px 0;">Awal Mula & Perkembangan</h3>
        <p style="font-size: 14px; line-height: 1.7; color: #475569; margin-bottom: 16px;">
          MASTER TRUCK didirikan pada tahun 2000 berawal dari inisiatif untuk memfokuskan jalur distribusi pelumas terkemuka <strong>Federal Oil</strong> di wilayah Sumatera Utara.
        </p>
        <p style="font-size: 14px; line-height: 1.7; color: #475569; margin: 0;">
          Seiring berjalannya waktu dan meningkatnya kepercayaan pelaku industri, perusahaan memperluas portofolio produk ke sektor aki, ban, dan sparepart mesin, sekaligus mengekspansi jaringan operasional hingga mencakup seluruh Pulau Sumatera (SUMBAGUT & SUMBAGSEL).
        </p>
      </div>

      <!-- Card Nilai & Visi -->
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 32px;">
        <div style="display: inline-block; background: #CCFBF1; color: #0F766E; font-weight: 700; font-size: 12px; padding: 4px 12px; border-radius: 6px; margin-bottom: 16px;">
          VISI & NILAI UNGGULAN
        </div>
        <h3 style="font-size: 20px; font-weight: 700; color: #0F172A; margin: 0 0 14px 0;">Integritas & Keandalan Logistik</h3>
        <p style="font-size: 14px; line-height: 1.7; color: #475569; margin-bottom: 14px;">
          <strong>Visi:</strong> Menjadi penyedia suku cadang dan pelumas pilihan utama di Indonesia dengan standardisasi OEM terbaik dan rantai pasok modern.
        </p>
        <ul style="font-size: 14px; line-height: 1.7; color: #475569; padding-left: 20px; margin: 0;">
          <li style="margin-bottom: 6px;"><strong>Keaslian Terjamin:</strong> Seluruh produk dipasok langsung dari pabrikan resmi tanpa perantara.</li>
          <li style="margin-bottom: 6px;"><strong>Kecepatan Pengiriman:</strong> Hub pergudangan strategis memastikan armada Anda tidak terhenti karena kendala part.</li>
          <li><strong>Digitalisasi Layanan:</strong> Dukungan penuh integrasi monitoring armada fleet melalui portal modern.</li>
        </ul>
      </div>

    </div>

  </div>
</section>

<!-- SECTION 2: BARANG & PRODUK RESMI (KATALOG DISTRIBUSI) -->
<section id="produk" style="padding: 80px 24px; background: #F1F5F9; color: #0F172A; border-top: 1px solid #E2E8F0;">
  <div style="max-width: 1200px; margin: 0 auto;">
    
    <div style="text-align: center; max-width: 760px; margin: 0 auto 50px auto;">
      <span style="color: #0D9488; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 8px;">KATALOG RESMI</span>
      <h2 style="font-size: 34px; font-weight: 800; color: #0F172A; margin: 0 0 16px 0; letter-spacing: -0.5px;">Produk & Komponen yang Didistribusikan</h2>
      <p style="font-size: 16px; color: #475569; line-height: 1.6;">
        Produk pilihan berstandar internasional untuk kendaraan roda dua, roda empat, armada komersial, dan sektor industri.
      </p>
    </div>

    <!-- Product 4-Grid Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px;">
      
      <!-- Card 1: Oli -->
      <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 28px; margin-bottom: 12px;">🛢️</div>
          <span style="font-size: 11px; font-weight: 700; color: #0284C7; text-transform: uppercase; letter-spacing: 1px;">Kategori Pelumas</span>
          <h3 style="font-size: 19px; font-weight: 700; color: #0F172A; margin: 6px 0 12px 0;">Oli Mesin & Transmisi</h3>
          <p style="font-size: 13px; line-height: 1.6; color: #475569; margin-bottom: 16px;">
            Pelumas bermutu tinggi dengan formulasi perlindungan gesekan mesin dan efisiensi konsumsi bahan bakar.
          </p>
        </div>
        <div style="background: #F8FAFC; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 12px;">
          <span style="font-size: 11px; color: #64748B; font-weight: 600; display: block; margin-bottom: 4px;">MEREK RESMI:</span>
          <span style="font-size: 14px; font-weight: 700; color: #0F172A;">Federal Oil</span>
        </div>
      </div>

      <!-- Card 2: Aki -->
      <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 28px; margin-bottom: 12px;">🔋</div>
          <span style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 1px;">Kategori Elektrikal</span>
          <h3 style="font-size: 19px; font-weight: 700; color: #0F172A; margin: 6px 0 12px 0;">Aki & Baterai Kendaraan</h3>
          <p style="font-size: 13px; line-height: 1.6; color: #475569; margin-bottom: 16px;">
            Aki Maintenance Free (MF) & aki basah berteknologi mutakhir dengan daya starter andal di segala kondisi cuaca.
          </p>
        </div>
        <div style="background: #F8FAFC; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 12px;">
          <span style="font-size: 11px; color: #64748B; font-weight: 600; display: block; margin-bottom: 4px;">MEREK RESMI:</span>
          <span style="font-size: 14px; font-weight: 700; color: #0F172A;">Furukawa Battery (FB)</span>
        </div>
      </div>

      <!-- Card 3: Ban -->
      <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 28px; margin-bottom: 12px;">🛞</div>
          <span style="font-size: 11px; font-weight: 700; color: #D97706; text-transform: uppercase; letter-spacing: 1px;">Kategori Roda & Ban</span>
          <h3 style="font-size: 19px; font-weight: 700; color: #0F172A; margin: 6px 0 12px 0;">Ban Motor, Mobil & Truk</h3>
          <p style="font-size: 13px; line-height: 1.6; color: #475569; margin-bottom: 16px;">
            Daya tahan jarak tempuh ekstra, traksi maksimal di jalan basah dan kering, serta efisiensi biaya operasional armada.
          </p>
        </div>
        <div style="background: #F8FAFC; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 12px;">
          <span style="font-size: 11px; color: #64748B; font-weight: 600; display: block; margin-bottom: 4px;">MEREK RESMI:</span>
          <span style="font-size: 14px; font-weight: 700; color: #0F172A;">Michelin • Indotube • Kaizen</span>
        </div>
      </div>

      <!-- Card 4: Sparepart -->
      <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="font-size: 28px; margin-bottom: 12px;">⚙️</div>
          <span style="font-size: 11px; font-weight: 700; color: #7C3AED; text-transform: uppercase; letter-spacing: 1px;">Kategori Suku Cadang</span>
          <h3 style="font-size: 19px; font-weight: 700; color: #0F172A; margin: 6px 0 12px 0;">Sparepart & Lampu OEM</h3>
          <p style="font-size: 13px; line-height: 1.6; color: #475569; margin-bottom: 16px;">
            Piston kit, kampas rem, suspensi, dan sistem pencahayaan halogen serta LED otomotif berstandar internasional.
          </p>
        </div>
        <div style="background: #F8FAFC; border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 12px;">
          <span style="font-size: 11px; color: #64748B; font-weight: 600; display: block; margin-bottom: 4px;">MEREK RESMI:</span>
          <span style="font-size: 13px; font-weight: 700; color: #0F172A;">RKN • Ichidai • Sachs • Philips • Osram</span>
        </div>
      </div>

    </div>

  </div>
</section>

<!-- SECTION 3: INTEGRASI WEB FLEET (PORTAL ARMASA) -->
<section id="fleet" style="padding: 80px 24px; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FFFFFF;">
  <div style="max-width: 1200px; margin: 0 auto;">
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 40px; align-items: center;">
      
      <div>
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(45, 212, 191, 0.15); border: 1px solid rgba(45, 212, 191, 0.3); padding: 4px 14px; border-radius: 50px; margin-bottom: 16px;">
          <span style="font-size: 11px; font-weight: 700; color: #5EEAD4; text-transform: uppercase;">PORTAL DIGITAL ARMASA</span>
        </div>

        <h2 style="font-size: 32px; font-weight: 800; line-height: 1.3; color: #FFFFFF; margin: 0 0 16px 0;">
          Terkoneksi Langsung dengan Sistem Web Fleet Customer
        </h2>

        <p style="font-size: 15px; line-height: 1.7; color: #94A3B8; margin-bottom: 24px;">
          Mitra pelanggan perusahaan dan pemilik armada perorangan dapat memantau seluruh proses servis, estimasi biaya, alur pengerjaan bengkel, dan riwayat pergantian suku cadang secara transparan.
        </p>

        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 30px;">
          <div style="display: flex; align-items: center; gap: 10px; font-size: 14px; color: #E2E8F0;">
            <span style="color: #2DD4BF; font-weight: bold;">✔</span> Lacak status servis kendaraan (Check-in, Inspeksi, Pengerjaan Mekanik, QC, hingga Gate Out).
          </div>
          <div style="display: flex; align-items: center; gap: 10px; font-size: 14px; color: #E2E8F0;">
            <span style="color: #2DD4BF; font-weight: bold;">✔</span> Validasi invoice dan persetujuan penawaran servis secara digital.
          </div>
          <div style="display: flex; align-items: center; gap: 10px; font-size: 14px; color: #E2E8F0;">
            <span style="color: #2DD4BF; font-weight: bold;">✔</span> Garansi ketersediaan komponen resmi MASTER TRUCK.
          </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 14px;">
          <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" style="background: #14B8A6; color: #FFFFFF; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 6px; text-decoration: none; display: inline-flex; align-items: center; gap: 8px;">
            <span>Masuk ke Web Fleet</span>
            <span>&rarr;</span>
          </a>
          <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" style="background: transparent; border: 1px solid #475569; color: #FFFFFF; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 6px; text-decoration: none;">
            Daftar Mitra Baru
          </a>
        </div>
      </div>

      <!-- Preview Mockup Card -->
      <div style="background: #090D16; border: 1px solid #334155; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1E293B; padding-bottom: 12px; margin-bottom: 16px;">
          <div style="display: flex; gap: 6px;">
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #EF4444; display: inline-block;"></span>
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #F59E0B; display: inline-block;"></span>
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
          </div>
          <span style="font-family: monospace; font-size: 11px; color: #64748B;">portal.lotuspradipta.co.id/fleet</span>
        </div>
        <div style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
          <div style="background: #1E293B; border-radius: 6px; padding: 12px; margin-bottom: 10px; border-left: 3px solid #2DD4BF;">
            <strong style="color: #FFFFFF; display: block;">Unit BK 8821 XA - Truk Tronton</strong>
            <span style="font-size: 11px; color: #2DD4BF;">Status: Sedang Pengerjaan Mekanik • Estimasi Selesai Hari Ini</span>
          </div>
          <div style="background: #1E293B; border-radius: 6px; padding: 12px; margin-bottom: 10px; border-left: 3px solid #38BDF8;">
            <strong style="color: #FFFFFF; display: block;">Unit BG 9021 LP - Mobil Niaga</strong>
            <span style="font-size: 11px; color: #38BDF8;">Status: QC Final & Uji Jalan • Lolos Inspeksi</span>
          </div>
          <div style="background: #1E293B; border-radius: 6px; padding: 12px; border-left: 3px solid #10B981;">
            <strong style="color: #FFFFFF; display: block;">Unit BL 4120 MM - Pickup Operasional</strong>
            <span style="font-size: 11px; color: #10B981;">Status: Selesai Servis • Gate Out Pass Ready</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</section>

<!-- SECTION 4: HUB KANTOR UTAMA & WILAYAH OPERASIONAL -->
<section id="kontak" style="padding: 80px 24px; background: #FFFFFF; color: #0F172A;">
  <div style="max-width: 1200px; margin: 0 auto;">
    
    <div style="text-align: center; max-width: 760px; margin: 0 auto 50px auto;">
      <span style="color: #0D9488; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 8px;">JARINGAN OPERASIONAL</span>
      <h2 style="font-size: 34px; font-weight: 800; color: #0F172A; margin: 0 0 16px 0; letter-spacing: -0.5px;">Kantor Utama & Hub Distribusi Regional</h2>
      <p style="font-size: 16px; color: #475569; line-height: 1.6;">
        Pusat logistik dan pergudangan terpadu untuk memastikan pasokan suku cadang selalu tersedia dan tepat waktu.
      </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px;">
      
      <!-- Kantor Utama -->
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 32px;">
        <span style="font-size: 24px; margin-bottom: 8px; display: block;">📍</span>
        <h3 style="font-size: 20px; font-weight: 700; color: #0F172A; margin: 0 0 12px 0;">Kantor Pusat & Pergudangan Utama</h3>
        <p style="font-size: 14px; line-height: 1.7; color: #475569; margin-bottom: 16px;">
          <strong>Komplek Pergudangan Palembang Star 1, Blok E5</strong><br>
          Jl. Pulau Bunaken Komplek Warehouse KIM III No. 3A, Mabar, Kec. Medan Labuhan, Kota Medan, Sumatera Utara 20242.
        </p>
        <div style="font-size: 13px; color: #64748B;">
          <strong>Legalitas:</strong> Terdaftar Resmi di Kementerian Perdagangan Republik Indonesia.
        </div>
      </div>

      <!-- Jangkauan Distribusi -->
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 32px;">
        <span style="font-size: 24px; margin-bottom: 8px; display: block;">🌐</span>
        <h3 style="font-size: 20px; font-weight: 700; color: #0F172A; margin: 0 0 12px 0;">Jangkauan Distribusi Sumatera</h3>
        
        <div style="margin-bottom: 14px;">
          <strong style="font-size: 14px; color: #0284C7; display: block; margin-bottom: 4px;">Region SUMBAGUT:</strong>
          <span style="font-size: 13px; color: #475569;">Medan (Sumatera Utara), Aceh, dan Pekanbaru (Riau).</span>
        </div>

        <div>
          <strong style="font-size: 14px; color: #0D9488; display: block; margin-bottom: 4px;">Region SUMBAGSEL:</strong>
          <span style="font-size: 13px; color: #475569;">Palembang (Sumatera Selatan), Lampung, Jambi, Bengkulu, dan Bangka Belitung.</span>
        </div>
      </div>

    </div>

  </div>
</section>

<!-- FOOTER -->
<footer style="background: #090D16; color: #94A3B8; padding: 50px 24px 30px 24px; border-top: 1px solid #1E293B;">
  <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px;">
    <div>
      <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; margin-bottom: 6px;">MASTER TRUCK</div>
      <div style="font-size: 12px; color: #64748B;">Distributor Resmi Nasional Pelumas, Aki, Ban & Suku Cadang Otomotif</div>
    </div>
    <div style="display: flex; gap: 20px; font-size: 13px;">
      <a href="http://localhost:3000/#login" target="_blank" rel="noopener noreferrer" style="color: #2DD4BF; text-decoration: none; font-weight: 600;">Login Web Fleet</a>
      <a href="http://localhost:3000/#register" target="_blank" rel="noopener noreferrer" style="color: #2DD4BF; text-decoration: none; font-weight: 600;">Daftar Mitra Armada</a>
    </div>
  </div>
  <div style="max-width: 1200px; margin: 30px auto 0 auto; padding-top: 20px; border-top: 1px solid #1E293B; font-size: 12px; text-align: center; color: #475569;">
    &copy; 2026 MASTER TRUCK. Hak Cipta Dilindungi Undang-Undang. Terdaftar di Kemendag RI.
  </div>
</footer>
HTML;

// 2. Buat atau update halaman Beranda
$page_data = [
    'post_title'    => 'Beranda - MASTER TRUCK',
    'post_name'     => 'beranda',
    'post_content'  => $page_content,
    'post_status'   => 'publish',
    'post_type'     => 'page',
    'comment_status'=> 'closed',
    'ping_status'   => 'closed',
];

if ($existing_page) {
    $page_data['ID'] = $existing_page->ID;
    $page_id = wp_update_post($page_data);
    echo "Halaman Beranda berhasil diperbarui (ID: {$page_id})\n";
} else {
    $page_id = wp_insert_post($page_data);
    echo "Halaman Beranda berhasil dibuat (ID: {$page_id})\n";
}

// 3. Konfigurasi Elementor Meta agar bisa langsung di-edit menggunakan Elementor!
update_post_meta($page_id, '_elementor_edit_mode', 'builder');
update_post_meta($page_id, '_elementor_template_type', 'wp-page');
update_post_meta($page_id, '_wp_page_template', 'elementor_header_footer');

// 4. Jadikan halaman ini sebagai Halaman Depan (Homepage) WordPress
update_option('show_on_front', 'page');
update_option('page_on_front', $page_id);

echo "Berhasil mengatur Beranda sebagai Homepage utama WordPress!\n";
