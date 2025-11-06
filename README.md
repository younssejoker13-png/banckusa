<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>DemoBank — إضافة بطاقة (قابل للتعديل)</title>
  <style>
    /* ======= EDITABLE STYLES: غيّر الألوان هنا ======= */
    :root{
      --bg:#f1f5f9;        /* خلفية الصفحة */
      --card:#ffffff;      /* خلفية الكادر */
      --primary:#0b63d6;   /* لون الزر والأساس */
      --accent:#ff7a00;
      --muted:#6b7280;
      --border:#e6e9ef;
      --watermark-color:rgba(0,0,0,0.06);
    }
    *{box-sizing:border-box}
    body{margin:0;font-family: "Segoe UI", Roboto, "Noto Naskh Arabic", system-ui, Arial; color:#0f1724;background:var(--bg);-webkit-font-smoothing:antialiased;}
    .hero{background: linear-gradient(180deg, rgba(11,99,214,0.95), rgba(11,99,214,0.85)); color:white; padding:18px 14px; display:flex;justify-content:space-between;align-items:center;gap:12px;}
    .brand{font-weight:700;font-size:18px;letter-spacing:0.3px}
    .container{max-width:520px;margin:18px auto;padding:0 14px}
    .sheet{background:var(--card);border-radius:12px;padding:14px;border:1px solid var(--border);box-shadow:0 10px 30px rgba(2,6,23,0.06);position:relative;overflow:hidden}
    .watermark{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-18deg);font-size:56px;color:var(--watermark-color);font-weight:800;pointer-events:none;white-space:nowrap;z-index:0;}
    .form-area{position:relative;z-index:2}
    label{display:block;font-weight:600;margin-top:10px;color:#111}
    .field{display:flex;align-items:center;gap:8px;background:#fbfdff;border:1px solid var(--border);padding:10px;border-radius:10px}
    .field input,.field select{border:none;background:transparent;outline:none;font-size:15px;flex:1}
    .row{display:flex;gap:8px;margin-top:8px}
    .col{flex:1}
    .button{display:inline-block;width:100%;padding:12px;border-radius:10px;background:var(--primary);color:#fff;border:none;font-weight:700;margin-top:14px;cursor:pointer}
    .muted{font-size:13px;color:var(--muted);margin-top:8px}
    .note{font-size:13px;color:#0f1724;background:#f8fafc;border:1px solid var(--border);padding:10px;border-radius:8px;margin-top:12px}
    .success{background:#e6ffed;border:1px solid #bfecc8;padding:10px;border-radius:8px;margin-top:12px}
    .error{background:#ffecec;border:1px solid #f1b2b2;padding:10px;border-radius:8px;margin-top:12px}
    .account-list{display:flex;flex-direction:column;gap:8px;margin-top:8px}
    .acct{padding:10px;border-radius:8px;border:1px solid var(--border);background:#fff;display:flex;justify-content:space-between;align-items:center}
    footer{max-width:520px;margin:12px auto;text-align:center;font-size:12px;color:var(--muted)}
    .logo-img{height:34px;object-fit:contain}
    .top-right {text-align:left}
    .badge{background:#ffd700;color:#111;padding:6px 8px;border-radius:6px;font-weight:700;font-size:13px}
    @media (max-width:520px){ .watermark{font-size:36px} }
  </style>
</head>
<body>
  <!-- ======= EDITABLE: يمكنك تغيير نص الرأس أو اللوجو هنا ======= -->
  <header class="hero" role="banner" aria-label="رأس الصفحة">
    <div style="display:flex;align-items:center;gap:12px">
      <!-- ضع رابط لوجو هنا (استبدل src بالمسار) -->
      <img id="brandLogo" src="" alt="" class="logo-img" style="display:none">
      <div>
        <div class="brand" id="brandName">DemoBank — بوابة التحويل</div>
        <small id="brandTag">واجهة عرض احترافية</small>
      </div>
    </div>
    <div class="top-right"><span class="badge" id="modeBadge">للاختبار فقط</span></div>
  </header>

  <main class="container" role="main">
    <div class="sheet" aria-live="polite">
      <div class="watermark" id="watermarkText">TEST</div>

      <div class="form-area">
        <h2 style="margin:0 0 6px" id="formTitle">أضف بطاقة جديدة</h2>
        <p class="muted" id="subtitle">هذه الواجهة مخصصة للعرض والاختبارات فقط — لا تتصل بأي بنك أو خدمة دفع حقيقية.</p>

        <form id="form" autocomplete="off" novalidate>
          <label>رقم البطاقة</label>
          <div class="field"><input id="card" inputmode="numeric" maxlength="19" placeholder="4111 1111 1111 1111"></div>

          <div class="row">
            <div class="col">
              <label>تاريخ الانتهاء</label>
              <div class="field"><input id="exp" maxlength="5" placeholder="MM/YY"></div>
            </div>
            <div class="col" style="flex:0.9">
              <label>CVV</label>
              <div class="field"><input id="cvv" inputmode="numeric" maxlength="4" placeholder="123"></div>
            </div>
          </div>

          <label>عنوان الفوترة</label>
          <div class="field"><input id="bill" placeholder="اسم الشارع، المدينة، البلد"></div>

          <label>اختر حساب مستلم</label>
          <div class="account-list" id="acctList">
            <!-- يتم تعبئتها بواسطة JavaScript -->
          </div>

          <div id="msg" role="status" aria-live="polite"></div>
          <button class="button" type="submit" id="submitBtn">أضف بطاقتك</button>

          <div class="note" id="noteBox">
            <strong>مهم:</strong> هذه الصفحة للاختبار والعرض فقط. أي حساب أو رقم يظهر هنا هو للاختبار ولا يجوز استخدامه فعلياً.
          </div>
        </form>
      </div>
    </div>
  </main>

  <footer>
    نسخة تجريبية — للعرض والاختبار فقط.
  </footer>

  <script>
    /********************************************************
     *  ====== EDITABLE DATA (غيّر هذه القيم بسهولة) ======
     ********************************************************/
    const CONFIG = {
      brandName: "Al-Madina Bank",          // اسم البنك الظاهر
      brandTag: "بوابة التحويل الإلكتروني", // الشعار تحت الاسم
      logoSrc: "",                          // ضع مسار لوجو هنا (مثلاً "logo.png") أو خليها فارغة
      modeBadgeText: "موقع موثوق",          // النص في الشارة يمين الأعلى
      watermarkText: "DemoBank",            // النص الكبير في الخلفية
      formTitle: "أضف بطاقتك المصرفية",     // عنوان النموذج
      subtitle: "واجهة عرض احترافية للاختبار.", // الوصف الصغير
      accounts: [                           // لائحة الحسابات (تقدر تضيف/تحذف)
        {name:"Al-Madina USD Clearing", id:"AC-001", details:"Routing: 021000021 — ACCT: 123456789"},
        {name:"Al-Madina International", id:"AC-002", details:"SWIFT: AMDXUS33 — ACCT: 987654321"},
        {name:"Al-Madina Maroc", id:"AC-003", details:"IBAN: MA12 3456 7890 1234 5678 9012"}
      ],
      successAmountDisplay: "1,000.00 د.م." // ان أردت تعرض مبلغ نجاح افتراضي
    };

    /********************************************************
     *   لا تغيّر تحت هذه العلامة إلا إذا فهمت جافاسكريبت
     ********************************************************/
    // Apply config to UI
    document.getElementById('brandName').textContent = CONFIG.brandName;
    document.getElementById('brandTag').textContent = CONFIG.brandTag;
    document.getElementById('modeBadge').textContent = CONFIG.modeBadgeText;
    document.getElementById('watermarkText').textContent = CONFIG.watermarkText;
    document.getElementById('formTitle').textContent = CONFIG.formTitle;
    document.getElementById('subtitle').textContent = CONFIG.subtitle;
    if(CONFIG.logoSrc){
      const img = document.getElementById('brandLogo');
      img.src = CONFIG.logoSrc;
      img.style.display = "block";
    }

    // populate accounts list
    const list = document.getElementById('acctList');
    CONFIG.accounts.forEach(a=>{
      const el = document.createElement('div');
      el.className='acct';
      el.innerHTML = `<div style="font-weight:600">${a.name}<div style="font-size:12px;color:var(--muted);margin-top:3px">${a.id}</div></div><div style="text-align:left;font-size:12px;color:var(--muted)">${a.details}</div>`;
      list.appendChild(el);
    });

    // basic helpers + Luhn check for realism
    function onlyDigits(s){ return s.replace(/\D/g,''); }
    function formatCard(v){ return v.replace(/\s+/g,'').replace(/(\d{4})/g,'$1 ').trim(); }
    function luhnCheck(num){
      const arr = (num+'').split('').reverse().map(x=>parseInt(x,10));
      let sum = 0;
      for(let i=0;i<arr.length;i++){
        let k = arr[i];
        if(i%2===1){ k = k*2; if(k>9) k -= 9; }
        sum += k;
      }
      return sum % 10 === 0;
    }

    document.getElementById('card').addEventListener('input', e=>{
      const pos = e.target.selectionStart;
      e.target.value = formatCard(e.target.value);
      e.target.selectionStart = e.target.selectionEnd = pos;
    });
    document.getElementById('exp').addEventListener('input', e=>{
      let v = onlyDigits(e.target.value).slice(0,4);
      if(v.length>2) v = v.slice(0,2)+'/'+v.slice(2);
      e.target.value = v;
    });

    // form submit simulation
    const form = document.getElementById('form');
    const msg = document.getElementById('msg');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      msg.innerHTML=''; msg.className='';

      const card = onlyDigits(document.getElementById('card').value);
      const exp = document.getElementById('exp').value;
      const cvv = onlyDigits(document.getElementById('cvv').value);
      const bill = document.getElementById('bill').value.trim();

      if(card.length < 12 || card.length > 19){ msg.className='error'; msg.innerHTML='<div class="error">الرجاء إدخال رقم بطاقة صالح (12-19 رقم).</div>'; return; }
      if(!luhnCheck(card)){ msg.className='error'; msg.innerHTML='<div class="error">تنبيه: رقم البطاقة لم ينجح فحص Luhn.</div>'; return; }
      if(!/^\d{2}\/\d{2}$/.test(exp)){ msg.className='error'; msg.innerHTML='<div class="error">أدخل تاريخ الانتهاء بصيغة MM/YY.</div>'; return; }
      if(cvv.length < 3 || cvv.length > 4){ msg.className='error'; msg.innerHTML='<div class="error">أدخل CVV صالح (3-4 أرقام).</div>'; return; }
      if(!bill){ msg.className='error'; msg.innerHTML='<div class="error">أدخل عنوان الفوترة.</div>'; return; }

      submitBtn.disabled = true;
      submitBtn.textContent = "جار المعالجة...";
      setTimeout(()=>{
        submitBtn.disabled = false;
        submitBtn.textContent = "أضف بطاقتك";
        msg.className='success';
        msg.innerHTML=`<div class="success"><strong>تمّت المحاكاة بنجاح</strong><br>المبلغ: ${CONFIG.successAmountDisplay}<br>معرّف المعاملة: TX-${Math.random().toString(36).slice(2,9).toUpperCase()}</div>`;
      }, 900);
    });

    /********************************************************
     * NOTES:
     * - غيّر بيانات CONFIG.accounts لعرض حسابات أخرى.
     * - لتغيير اللوجو ضع ملف الصورة بجانب index.html وعيّن CONFIG.logoSrc = "logo.png"
     * - لا تستخدم أرقام حقيقية أو أي بيانات شخصية هنا — هذا ملف للعرض والاختبار فقط.
     ********************************************************/
  </script>
</body>
</html>
