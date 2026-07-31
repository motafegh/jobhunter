from jobhunter.jobinja_details import parse_jobinja_detail


def test_parses_json_ld_and_explicit_jobinja_sections() -> None:
    html = """
    <html lang="fa">
      <head>
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "JobPosting",
          "title": "توسعه دهنده هوش مصنوعی (AI Developer)",
          "description": "<p>ساخت سرویس های Python و Machine Learning</p>",
          "hiringOrganization": {"@type": "Organization", "name": "آسه تجارت آسیا"},
          "jobLocation": {"address": {"addressLocality": "تهران", "addressCountry": "IR"}},
          "employmentType": "FULL_TIME",
          "datePosted": "2026-07-01",
          "validThrough": "2026-08-01",
          "skills": ["Python", "Machine Learning"]
        }
        </script>
      </head>
      <body>
        <h1>توسعه دهنده هوش مصنوعی (AI Developer)</h1>
        <div>دسته‌بندی شغلی</div><div>وب، برنامه‌نویسی و نرم‌افزار</div>
        <div>حداقل سابقه کار</div><div>سه سال</div>
        <div>حداقل مدرک تحصیلی</div><div>کارشناسی</div>
        <div>جنسیت</div><div>تفاوتی ندارد</div>
        <div>وضعیت نظام وظیفه</div><div>معافیت دائم یا پایان خدمت</div>
      </body>
    </html>
    """

    detail = parse_jobinja_detail(html)

    assert detail.title == "توسعه دهنده هوش مصنوعی (AI Developer)"
    assert detail.company == "آسه تجارت آسیا"
    assert detail.location == "تهران، IR"
    assert detail.employment_type == "FULL_TIME"
    assert detail.minimum_experience == "سه سال"
    assert detail.education == "کارشناسی"
    assert detail.description == "ساخت سرویس های Python و Machine Learning"
    assert detail.skills == ("Python", "Machine Learning")
    assert detail.language == "mixed"


def test_falls_back_to_persian_label_sections() -> None:
    html = """
    <main>
      <h1>مهندس امنیت</h1>
      <section>موقعیت مکانی</section><div>تهران، تهران</div>
      <section>نوع همکاری</section><div>تمام‌وقت</div>
      <section>شرح موقعیت شغلی</section>
      <p>طراحی و نگهداری ابزارهای امنیتی</p>
      <section>مهارت‌های مورد نیاز</section>
      <div>Python</div><div>Linux</div>
      <section>معرفی شرکت</section><p>یک شرکت فناوری</p>
    </main>
    """

    detail = parse_jobinja_detail(html)

    assert detail.title == "مهندس امنیت"
    assert detail.location == "تهران، تهران"
    assert detail.employment_type == "تمام‌وقت"
    assert detail.description == "طراحی و نگهداری ابزارهای امنیتی"
    assert detail.skills == ("Python", "Linux")
    assert detail.company_description == "یک شرکت فناوری"


def test_prefers_visible_jobinja_scalars_and_ignores_following_page_ui() -> None:
    html = """
    <html>
      <head>
        <script type="application/ld+json">
        {
          "@type": "JobPosting",
          "title": "AI Developer",
          "description": "Build AI systems",
          "jobLocation": {
            "address": {
              "addressCountry": {"@type": "Country", "name": "IR"}
            }
          },
          "employmentType": "FULL_TIME",
          "baseSalary": {"value": 5000000}
        }
        </script>
      </head>
      <body>
        <h1>AI Developer</h1>
        <section>موقعیت مکانی</section><div>تهران</div>
        <section>نوع همکاری</section><div>تمام‌وقت و حضوری</div>
        <section>حقوق</section><div>۵ میلیون تومان در ماه</div>
        <section>حداقل مدرک تحصیلی</section><div>کارشناسی</div>
        <div>مشاغل مشابه</div>
        <div>اطلاع‌رسانی از طریق ایمیل</div>
        <div>پشتیبان سایت</div>
      </body>
    </html>
    """

    detail = parse_jobinja_detail(html)

    assert detail.location == "تهران"
    assert detail.employment_type == "تمام‌وقت و حضوری"
    assert detail.salary == "۵ میلیون تومان در ماه"
    assert detail.education == "کارشناسی"
