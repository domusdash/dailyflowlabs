document.addEventListener('DOMContentLoaded', () => {
  
  // --- 1. Fallback Scroll Listener for Header (Firefox/Older Safari) ---
  if (!CSS.supports('(animation-timeline: scroll()) and (animation-range: 0% 100%)')) {
    const header = document.querySelector('header');
    
    const handleScroll = () => {
      if (window.scrollY > 40) {
        header.style.height = '64px';
        header.style.background = 'rgba(3, 3, 3, 0.75)';
        header.style.backdropFilter = 'blur(16px)';
        header.style.webkitBackdropFilter = 'blur(16px)';
        header.style.borderBottom = '1px solid rgba(255, 255, 255, 0.08)';
      } else {
        header.style.height = '90px';
        header.style.background = 'transparent';
        header.style.backdropFilter = 'none';
        header.style.webkitBackdropFilter = 'none';
        header.style.borderBottom = '1px solid transparent';
      }
    };
    
    // Run initially and bind to scroll
    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
  }

  // --- 2. IntersectionObserver for Reveal Animations ---
  const revealElements = document.querySelectorAll('.reveal');
  
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target); // Reveal once
        }
      });
    }, {
      root: null,
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback if IntersectionObserver is not supported
    revealElements.forEach(el => el.classList.add('revealed'));
  }

  // --- 3. Interactive Product Card Mockups ---
  // DomusDash Card Hover Micro-Interactions (Chore Toggling)
  const domusCard = document.querySelector('.product-card-domus');
  const choreCheckboxes = document.querySelectorAll('.mockup-chores .chore-row');
  
  if (domusCard && choreCheckboxes.length > 0) {
    domusCard.addEventListener('mouseenter', () => {
      // Temporarily toggle checking items as a playful interaction
      const secondChore = choreCheckboxes[1]; // "Feed the dog"
      const checkbox = secondChore.querySelector('.chore-check');
      const text = secondChore.querySelector('span:not(.chore-check)');
      
      setTimeout(() => {
        if (domusCard.matches(':hover')) {
          checkbox.classList.add('chore-check-checked');
          text.style.textDecoration = 'line-through';
          text.style.color = 'var(--text-muted)';
        }
      }, 500);
    });
    
    domusCard.addEventListener('mouseleave', () => {
      // Revert chore to original state
      const secondChore = choreCheckboxes[1];
      const checkbox = secondChore.querySelector('.chore-check');
      const text = secondChore.querySelector('span:not(.chore-check)');
      
      checkbox.classList.remove('chore-check-checked');
      text.style.textDecoration = 'none';
      text.style.color = 'var(--text-secondary)';
    });
  }

  // IronDial Card Hover Micro-Interactions (Vital Pulse & Set Increment)
  const ironCard = document.querySelector('.product-card-iron');
  const vitalNumber = document.querySelector('.mockup-vital-num');
  
  if (ironCard && vitalNumber) {
    let originalText = vitalNumber.innerHTML;
    
    ironCard.addEventListener('mouseenter', () => {
      // Animate vitals tracking reading changing
      let count = 785;
      const target = 812;
      const duration = 600; // ms
      const stepTime = Math.abs(Math.floor(duration / (target - count)));
      
      const timer = setInterval(() => {
        count++;
        vitalNumber.innerHTML = `${count} <span>ng/dL</span>`;
        if (count >= target) {
          clearInterval(timer);
        }
      }, stepTime);
      
      // Store interval ID on element to clear if mouse leaves early
      vitalNumber.dataset.intervalId = timer;
    });
    
    ironCard.addEventListener('mouseleave', () => {
      // Clear ongoing interval and restore original text
      if (vitalNumber.dataset.intervalId) {
        clearInterval(parseInt(vitalNumber.dataset.intervalId));
      }
      vitalNumber.innerHTML = originalText;
    });
  }

  // --- 4. Contact Form Handler (Simulated Submit with Success Feedback) ---
  const contactForm = document.getElementById('contactForm');
  const submitBtn = document.getElementById('submitBtn');
  const successMsg = document.getElementById('successMsg');
  
  if (contactForm && submitBtn && successMsg) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Validation check
      if (!contactForm.checkValidity()) {
        return;
      }
      
      // Disable inputs and button, show sending state
      submitBtn.disabled = true;
      const originalBtnHtml = submitBtn.innerHTML;
      submitBtn.innerHTML = 'Sending... <svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="animation: spin 1s linear infinite"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.2)"></circle><path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor"></path></svg>';
      
      // Add inline CSS keyframes for spinner if not present
      if (!document.getElementById('spinner-style')) {
        const style = document.createElement('style');
        style.id = 'spinner-style';
        style.innerHTML = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
        document.head.appendChild(style);
      }
      
      // Simulate network request (1.5 seconds)
      setTimeout(() => {
        // Hide button contents, show success message
        successMsg.style.display = 'block';
        contactForm.reset();
        
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
        
        // Scroll success message into view smoothly
        successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Hide success message after 7 seconds
        setTimeout(() => {
          successMsg.style.display = 'none';
        }, 7000);
      }, 1500);
    });
  }
});
