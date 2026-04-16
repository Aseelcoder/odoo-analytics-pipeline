import pandas as pd
from sqlalchemy import create_engine, text

# 1. إعدادات الاتصال
DB_CONFIG = {
    "user": "your_username",
    "password": "your_password", 
    "host": "localhost",
    "port": "your_port_number",
    "database": "your_database_name"
}

connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(connection_string)

def run_odoo_pipeline_etl():
    print("🚀 بدء عملية نقل البيانات...")

    # 2. الاستعلام (SQL) - قمنا بإضافة ->> 'en_US' لاستخراج النص من القاموس مباشرة
    query = """
    SELECT 
        l.id AS lead_id,
        l.name AS opportunity_name,
        COALESCE(l.expected_revenue, 0) AS revenue,
        COALESCE(l.probability, 0) AS success_probability,
        -- استخراج الاسم النصي للمرحلة من حقل JSON الخاص بالترجمة
        s.name->>'en_US' AS stage_name, 
        p.name AS customer_name,
        l.create_date AT TIME ZONE 'UTC' AS creation_date,
        (COALESCE(l.expected_revenue, 0) * (COALESCE(l.probability, 0) / 100)) AS weighted_revenue
    FROM 
        public.crm_lead l
    JOIN 
        public.crm_stage s ON l.stage_id = s.id
    LEFT JOIN 
        public.res_partner p ON l.partner_id = p.id
    WHERE 
        l.active = true;
    """

    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        if df.empty:
            print("⚠️ لا توجد بيانات لنقلها.")
            return

        # 3. معالجة إضافية (إذا لم ينجح الاستخراج من SQL)
        # للتأكد من أن أي قيم قاموس متبقية تحولت لنصوص
        df['stage_name'] = df['stage_name'].apply(lambda x: x['en_US'] if isinstance(x, dict) else x)

        # تحويل التواريخ
        df['creation_date'] = pd.to_datetime(df['creation_date'])
        df['last_sync_at'] = pd.Timestamp.now()

        # 4. التحميل إلى السكيما التحليلية
        df.to_sql(
            'crm_pipeline_report', 
            con=engine, 
            schema='odoo_analytics_dw', 
            if_exists='replace', 
            index=False
        )

        print("-" * 50)
        print(f"✅ تم بنجاح! تم نقل {len(df)} سجل.")
        print(f"📦 الجدول: odoo_analytics_dw.crm_pipeline_report")
        print("-" * 50)

    except Exception as e:
        print(f"❌ فشلت العملية: {e}")

if __name__ == "__main__":
    run_odoo_pipeline_etl()