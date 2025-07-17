"use client";

import { useLanguage } from '@/lib/language-context';
import Link from 'next/link';
import { Facebook, Twitter, Instagram, Mail, Phone, MapPin } from 'lucide-react';

export default function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Hospital Branding */}
          <div>
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <svg className="h-8 w-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v4h4v2h-4v4h-2v-4H7v-2h4V7z"/>
              </svg>
              {t('footer.hospital_name')}
            </h2>
            <p className="text-gray-300 text-sm">
              {t('footer.description')}
            </p>
          </div>

          {/* Navigation Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-blue-400">{t('footer.quick_links')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-blue-400 transition-colors">
                  {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link href="/patient-portal" className="text-gray-300 hover:text-blue-400 transition-colors">
                  {t('nav.patient_portal')}
                </Link>
              </li>
              <li>
                <Link href="/feedback" className="text-gray-300 hover:text-blue-400 transition-colors">
                  {t('nav.feedback')}
                </Link>
              </li>
              <li>
                <Link href="/services" className="text-gray-300 hover:text-blue-400 transition-colors">
                  {t('nav.services')}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-300 hover:text-blue-400 transition-colors">
                  {t('nav.contact')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-blue-400">{t('footer.contact')}</h3>
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <MapPin className="h-5 w-5 text-blue-400" />
                <span className="text-gray-300">BP 4856, Douala, Cameroon</span>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="h-5 w-5 text-blue-400" />
                <a href="tel:+237233501111" className="text-gray-300 hover:text-blue-400 transition-colors">
                  +237 233 50 11 11
                </a>
              </li>
              <li className="flex items-center gap-2">
                <Mail className="h-5 w-5 text-blue-400" />
                <a href="mailto:info@hgd.cm" className="text-gray-300 hover:text-blue-400 transition-colors">
                  info@hgd.cm
                </a>
              </li>
            </ul>
          </div>

          {/* Social Media & Newsletter */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-blue-400">{t('footer.follow_us')}</h3>
            <div className="flex gap-4 mb-6">
              <a
                href="https://facebook.com/hgdouala"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                <Facebook className="h-6 w-6" />
              </a>
              <a
                href="https://twitter.com/hgdouala"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                <Twitter className="h-6 w-6" />
              </a>
              <a
                href="https://instagram.com/hgdouala"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-300 hover:text-blue-400 transition-colors"
              >
                <Instagram className="h-6 w-6" />
              </a>
            </div>
            <h3 className="text-lg font-semibold mb-4 text-blue-400">{t('footer.newsletter')}</h3>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder={t('footer.newsletter_placeholder')}
                className="bg-gray-800 text-white border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 w-full max-w-xs"
              />
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                {t('footer.subscribe')}
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-gray-400 text-sm">
          <p>
            &copy; {new Date().getFullYear()} {t('footer.hospital_name')}. {t('footer.rights_reserved')}
          </p>
        </div>
      </div>
    </footer>
  );
}